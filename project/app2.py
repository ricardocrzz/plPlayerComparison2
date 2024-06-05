from flask import Flask, render_template, url_for, request, redirect
import os
import mysql.connector
from dbConfig import DBCONFIG

app=Flask(__name__)

#configure mysql
db=mysql.connector.connect(**DBCONFIG)
cursor=db.cursor()

#shortcut for interacting with db
def executeQuery(query, params=None):
    cursor.execute(query, params)
    db.commit()

def fetchTeams():
    cursor.execute('select * from teams')
    teams=cursor.fetchall()

    return teams

def fetchPositions():
    cursor.execute('select * from positions')
    positions=cursor.fetchall()

    return positions

def fetchData():
    cursor.execute('select * from playerInfo')
    playerInfo=cursor.fetchall()

    cursor.execute('select * from playerWages')
    playerWages=cursor.fetchall()

    cursor.execute('select * from gkStats')
    gkStats=cursor.fetchall()

    cursor.execute('select * from dfStats')
    dfStatss=cursor.fetchall()

    cursor.execute('select * from mfStats')
    mfStats=cursor.fetchall()

    cursor.execute('select * from fwStats')
    fwStats=cursor.fetchall()


    return [(info, wage, stat) for info in playerInfo for wage in playerWages 

    
    for stat in gkStats 
    for stat in dfStats
    for stat in mfStats
    for stat in fwStats
    
    if info[0] == wage[0] && info[1] == wage[1]]

@app.route('/compare')
def compare():
    firstPlayerId=request.args.get('firstPlayer')
    secondPlayerId=request.args.get('secondPlayer')
    try:
        query=f"select * from players where playerId = {firstPlayerId}"
        cursor.execute(query)
        firstPlayerData = cursor.fetchone()

        query=f"select * from wages where playerId = {firstPlayerId}"
        cursor.execute(query)
        firstPlayerWageData = cursor.fetchone()

        query=f"select * from players where playerId = {secondPlayerId}"
        cursor.execute(query)
        secondPlayerData = cursor.fetchone()

        query=f"select * from wages where playerId = {secondPlayerId}"
        cursor.execute(query)
        secondPlayerWageData = cursor.fetchone()

        if firstPlayerData and firstPlayerWageData and secondPlayerData and secondPlayerWageData:
            totalData = [(firstPlayerData, firstPlayerWageData), (secondPlayerData,secondPlayerWageData)]

        else:
            print(f"no first player found with id {firstPlayerId}")

        return render_template('comparePlayers.html', data=totalData)

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    return render_template('comparePlayers.html')  # Handle the case where an error occurs

@app.route('/choosePlayers', methods=['POST', 'GET'])
def choosePlayers():
    if request.method == 'POST':
        firstPlayer = request.form.get('firstPlayer')
        secondPlayer = request.form.get('secondPlayer')

        if firstPlayer and secondPlayer:
            print(firstPlayer)
            print(secondPlayer)
            return redirect('/result')

    totalData=fetchData()
    return render_template('showPlayers.html', data=totalData)

@app.route('/addPlayer', methods=['POST', 'GET'])
def addPlayer():
    if request.method == 'POST':
        playerId = request.form['playerId']
        name = request.form['name']
        teamId = request.form['teamId']
        nation = request.form['nation']
        fieldPos = request.form['fieldPos']
        age = request.form['age']

        #query
        query = 'insert into players (playerId, name, teamId, nation, fieldPos, age) values (%s, %s, %s, %s, %s, %s)'
        params = (playerId, name, teamId, nation, fieldPos, age)
        executeQuery(query, params)

        return redirect('/')
    else:
        return render_template('addPlayers.html')

@app.route('/addWage', methods=['POST', 'GET'])
def addWage():
    if request.method == 'POST':
        playerId = request.form['playerId']
        annual = request.form['annual']
        transfer = request.form['transfer']
        joined = request.form['joined']

        #query
        query = 'insert into wages (playerId, annual, transfer, joined) values (%s, %s, %s, %s)'
        params = (playerId, annual, transfer, joined)
        executeQuery(query, params)

        return redirect('/')
    else:
        return render_template('addPlayers.html')

@app.route('/')
def index():
    totalData=fetchData()
    return render_template('index.html', data=totalData)

if __name__ == '__main__':
    app.run(debug=True)