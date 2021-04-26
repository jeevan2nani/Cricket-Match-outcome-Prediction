from django.shortcuts import render
from django.http import HttpResponse
from .ML import project as pr
import csv
import os

def home(request) :
    return render(request,'home.html')

def index(request) :
    return render(request,'index.html')

def about(request) :
    return render(request,'us.html')

def encode_team(team):
    team_id=0
    if team =='Mumbai Indians':
        team_id=1
    elif team =='Kolkata Knight Riders':
        team_id=2
    elif team =='Royal Challengers Bangalore':
        team_id=3
    elif team =='Chennai Super Kings':
        team_id=5
    elif team =='Rajasthan Royals':
        team_id=6
    elif team =='Delhi Capitals':
        team_id=7
    elif team == 'Kings XI Punjab':
        team_id=9
    elif team =='Sunrisers Hyderabad':
        team_id=10
    return team_id

def encode_stadium(venue):
    venue_id=0
    if venue =='Wankhede Stadium, Mumbai':
        venue_id=1

    elif venue =='Eden Gardens, Kolkata':
        venue_id=2
    elif venue =='chinnaswamy stadium, Bangalore':
        venue_id=3
    elif venue =='M. A. Chidambaram Stadium, Chennai':
        venue_id=5
    elif venue =='Sawai Mansingh Stadium, Jaipur':
        venue_id=6
    elif venue =='Feroz Shah Kotla, Delhi':
        venue_id=7
    elif venue == 'PCA Stadium, Mohali':
        venue_id=9
    elif venue =='Rajiv Gandhi International Cricket Stadium, Hyderabad':
        venue_id=10
    return venue_id

def decode_team(team_id):
    team="ADB"
    if team_id==1:
        team ='Mumbai Indians'
    elif team_id==2:
        team ='Kolkata Knight Riders'
    elif team_id==3:
        team ='Royal Challengers Bangalore'
    elif team_id==5:
        team ='Chennai Super Kings'
    elif team_id==6 :
        team ='Rajasthan Royals'
    elif team_id==7:
        team ='Delhi Capitals'
    elif team_id==9:
        team ='Kings XI Punjab'
    elif team_id==10:
        team ='Sunrisers Hyderabad'
    return team

def predict(request):

    if request.method =='POST':
        team1 = request.POST.get('city1')
        team2 = request.POST.get('city2')
        venue = request.POST.get('venue')
        toss = request.POST.get('won')
        chose = request.POST.get('chose')
        print(team1)
        print(team2)
        print(venue)
        print(toss)
        print(chose)
        team1_id = encode_team(team1)
        print(team1_id)
        team2_id = encode_team(team2)
        print(team2_id)
        venue_id = encode_stadium(venue)
        print(venue_id)
        toss_id=0
        chose_id=0
        if toss == 'Team 1':
            toss_id=team1_id
        else :
            toss_id=team2_id
        if chose=='Bat':
            chose_id=1
        else :
            chose_id=0

        print('HI')
        print(os.getcwd())
        with open('test.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(['team1','team2','city','toss_winner','venue','toss_desicion'])
            filewriter.writerow([team1_id,team2_id,venue_id,toss_id,venue_id,chose_id])

        output=pr.execute();

        file = 'test.csv'
        if(os.path.exists(file) and os.path.isfile(file)):
            os.remove(file)
        name = decode_team(output)

        print(output)
        content = {'name':name,}
        return render(request,'result.html',content)
