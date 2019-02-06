from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from home.models import Home
from django.utils.http import is_safe_url
from django.utils.timezone import make_aware
import requests

from bs4 import BeautifulSoup
import datetime
import re
from difflib import SequenceMatcher


def regex_gen(re_string):
    return re.compile('.*' + re_string + '.*')


def link_analyser(url):
    source_code = requests.get(url, allow_redirects=False)
    plain_text = source_code.text.encode('ascii', 'replace')
    try:
        soup = BeautifulSoup(plain_text, 'html.parser')
    except Exception:
        pass
    return soup


def extract_link(data_with_link, tag='a'):
    link_analyser_item = []
    for link in data_with_link.findAll(tag):
        link_analyser_item.append(link.get('href'))
    return link_analyser_item


def extract_text(data_with_link, tag='a', extract_link_regex=None):
    data_string = []
    if extract_link_regex:
        for link in data_with_link.findAll(tag, {'class': extract_link_regex}):
            data_string.append(" ".join(str(link.string).split()))
    else:
        for link in data_with_link.findAll(tag):
            data_string.append(" ".join(str(link.string).split()))
    return data_string


def data_analyser(data, tag, da_regex_string):
    data_analyser_item = []
    data_analyser_regex = re.compile('.*' + da_regex_string + '.*')
    for item in data.findAll(tag, {'class': data_analyser_regex}):
        data_analyser_item.append(item)
    return data_analyser_item


def extract_date(evt_url, evt_time):
    time_now = datetime.datetime.now()
    event_in_range = 0
    time_gap_min = 0
    event_date_time = 0
    if evt_time and evt_url:
        event_in_range = False
        try:
            event_date_time = datetime.datetime(int(evt_url[9:13]), int(evt_url[14:16]), int(evt_url[17:19]), int(evt_time[:2]), int(evt_time[-2:]))
            time_gap = event_date_time - time_now
            time_gap_min = time_gap.days * 24 * 60 + time_gap.seconds // 60
            if 5 <= time_gap_min <= 7 * 24 * 60:
                event_in_range = True
        except ValueError:
            pass
    return event_in_range, time_gap_min, event_date_time


def betin(s_team):
    betin_link = None
    betin_url = 'https://web.betin.co.ke/Sport/OddsSearchResults.aspx?q=' + s_team.replace(' ', '+') + '&antepost=1'
    analyser_link4 = link_analyser(betin_url)
    for item13 in analyser_link4.findAll('td', {'class': 'ricercaSE'}):
        extracted_link3 = extract_link(item13)
        for betin_href in extracted_link3:
            if betin_href.startswith('/Sport'):
                betin_link = 'https://web.betin.co.ke' + betin_href
        if betin_link:
            break
    return betin_link


def add_games(request):
    home_url = 'https://www.soccerway.com'
    available_list = Home.objects.all().values_list('match_date')
    perc = 0.7
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None

    analyser_link1 = link_analyser(home_url)
    for item in analyser_link1.findAll('th', {'class': regex_gen('competition-link')}):
        extracted_link1 = extract_link(item)
        for each_link in extracted_link1:
            analyser_link2 = link_analyser(home_url+each_link)
            for item2 in analyser_link2.findAll('table', {'class': 'matches'}):
                for item3 in item2.findAll('tr', {'class': regex_gen('match no-date-repetition')}):
                    for item4 in item3.findAll('td', {'class': 'score-time status'}):
                        extracted_link2 = extract_link(item4)
                        extracted_text1 = extract_text(item4,  'span', 'timestamp')
                        for evt_time, item_url in zip(extracted_text1, extracted_link2):
                            evt_in_range, _, evt_date_time = extract_date(item_url, evt_time)
                            if not evt_date_time in available_list:
                                if evt_in_range and item_url and evt_time:
                                    team_info = {}
                                    for item5 in item3.findAll('td', {'class': 'team team-a'}):
                                        for home_team in extract_text(item5):
                                            team_info['home_team'] = home_team
                                    for item6 in item3.findAll('td', {'class': 'team team-b'}):
                                        for away_team in extract_text(item6):
                                            team_info['away_team'] = away_team
                                    team_info['match_date'] = make_aware(evt_date_time)
                                    team_info['soccerway_url'] = home_url+item_url

                                    analyser_link3 = link_analyser(home_url+item_url)
                                    total_teams = 0
                                    psn = 0
                                    name = None
                                    position_of = 0
                                    uib_data = 0
                                    for item16 in analyser_link3.findAll('div', {'class': 'yui-b'}):
                                        if uib_data == 1:
                                            for item17 in item16.findAll('h2'):
                                                league_link1 = home_url + extract_link(item17)[0]
                                            for item7 in item16.findAll('table', {'class': 'leaguetable sortable table'}):
                                                for item8 in analyser_link3.findAll('div', {'class': 'block_match_info real-content clearfix'}):
                                                    for item9 in item8.findAll('div', {'class': 'details clearfix'}):
                                                        league_link2 = home_url + extract_link(item9)[0]
                                                        if SequenceMatcher(a=league_link1, b=league_link2).ratio() > 0.9:
                                                            league_link = league_link2
                                                        else:
                                                            league_link = league_link1
                                                        ana_link = link_analyser(league_link)
                                                        for item10 in ana_link.findAll('table', {'class': 'leaguetable sortable table detailed-table'}):
                                                            for _ in item10.findAll('tr', {'class':  regex_gen('team_rank')}):
                                                                total_teams += 1
                                                        break
                                                for item12 in item7.findAll('tr', {'class': regex_gen('highlight')}):
                                                    for item13 in item12.findAll('td', {'class': regex_gen('rank')}):
                                                        position_of = int(item13.string)
                                                    for team_name in extract_text(item12):
                                                        name = team_name
                                                    smtc = SequenceMatcher(a=home_team, b=name).ratio()
                                                    try:
                                                        if smtc > 0.5:
                                                            psn -= position_of
                                                        else:
                                                            psn = position_of
                                                    except (TypeError, Exception):
                                                        pass
                                            try:
                                                total_teams -= 1
                                                score = psn/total_teams
                                            except (ZeroDivisionError, TypeError):
                                                score = 0
                                            if score >= perc:
                                                team_info['p_table_score'] = 'Home'
                                            elif score <= -perc:
                                                team_info['p_table_score'] = 'Away'
                                            else:
                                                team_info['p_table_score'] = None
                                            abs_score = abs(int(score*100))
                                            team_info['table_score'] = abs_score
                                            if team_info:
                                                hm_aw = ('left', 'right')
                                                wld_percentage = perc*0.7
                                                psn_gap = None
                                                for home_away in hm_aw:
                                                    for item14 in item8.findAll('div', {'class': 'container ' + home_away}):
                                                        for item15 in item14.findAll('div', {'class': 'form clearfix'}):
                                                            extracted_text2 = extract_text(item15)
                                                            lap = 0
                                                            total_score = 0
                                                            for outcome in extracted_text2:
                                                                lap += 1
                                                                if outcome == 'W':
                                                                    total_score += 16 - lap
                                                                if outcome == 'D':
                                                                    total_score += 5 + lap
                                                                if outcome == 'L':
                                                                    total_score += lap
                                                                if lap == 5:
                                                                    lap = 0
                                                    if total_score >= 0:
                                                        wdl_score = total_score - 15
                                                    else:
                                                        wdl_score = total_score + 15
                                                    if psn_gap:
                                                        psn_gap -= wdl_score
                                                    else:
                                                        psn_gap = wdl_score
                                                try:
                                                    wl_score = psn_gap/50
                                                except (ZeroDivisionError, TypeError):
                                                    wl_score = 0
                                                if wl_score >= wld_percentage:
                                                    team_info['p_last_five_score'] = 'Home'
                                                elif wl_score <= -wld_percentage:
                                                    team_info['p_last_five_score'] = 'Away'
                                                else:
                                                    team_info['p_last_five_score'] = None
                                                abs_wl_score = abs(int(wl_score*100))
                                                team_info['last_five_score'] = abs_wl_score
                                                if team_info:
                                                    bet_link = betin(home_team)
                                                    bet_link2 = betin(away_team)
                                            if bet_link:
                                                team_info['betin_url'] = bet_link
                                            else:
                                                team_info['betin_url'] = bet_link2
                                            try:
                                                new_Home = Home(**team_info)
                                                new_Home.save()
                                                print('saved')
                                            except Exception:
                                                pass
                                        uib_data += 1

    if is_safe_url(redirect_path, request.get_host()):
        return redirect(redirect_path)
    return redirect('home_page:index')


def delete_all(request):
    Home.objects.all().delete()
    return redirect('home_page:index')


class HomeListView(ListView):
    template_name = 'home/index.html'

    def get_queryset(self,*args,**kwargs):
        return Home.objects.all()
