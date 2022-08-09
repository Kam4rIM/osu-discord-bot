import requests
import discord

def get_token():
    user = open('osu.txt').readlines()
    URL = "https://osu.ppy.sh/oauth/token"

    body = {
        "client_id": int(user[0]),
        "client_secret": user[1],
        "grant_type": "client_credentials",
        "scope": "public"
    }

    response = requests.post(URL, data=body)
    return response.json().get('access_token')


def get_scores(user, mode='osu', limit=5, offset=0):
    token = get_token()

    URL = f'https://osu.ppy.sh/api/v2/users/{user}/scores/best'

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f'Bearer {token}'
    }

    params = {
        'mode': mode,
        'limit': limit,
        'offset': offset
    }

    return requests.get(URL, params=params, headers=headers).json()

def get_recent_score(user, mode='osu'):
    token = get_token()

    URL = f'https://osu.ppy.sh/api/v2/users/{user}/scores/recent'

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f'Bearer {token}'
    }

    params = {
        'mode': mode,
        'limit': 1,
        'offset': 0
    }

    return requests.get(URL, params=params, headers=headers).json()


def get_userid(nickname):
    URL = 'https://osu.ppy.sh/api/v2/search'
    token = get_token()

    params = {
        'mode': 'user',
        "query": nickname
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f'Bearer {token}'
    }

    response = requests.get(URL, params=params, headers=headers)
    return response.json()['user']['data'][0]['id']








ds_token = open('token.txt').readline()


client = discord.Client()


@client.event
async def on_message(message):
    channel = message.channel
    if message.content.startswith('!scores'):
        msg = ''
        data = message.content.split()
        user = data[1]
        if len(data) > 2:
            if data[2] == 'ctb':
                response = get_scores(get_userid(user), mode='fruits')
            elif data[2] == 'taiko':
                response = get_scores(get_userid(user), mode='taiko')
            elif data[2] == 'mania':
                response = get_scores(get_userid(user), mode='mania')
            else:
                response = get_scores(get_userid(user), mode='osu')
        else:
            response = get_scores(get_userid(user))
        print(response)
        player = response[0]['user']['username']
        mode = response[0]['mode']
        embed = discord.Embed(title=f'Top scores of {player} in {mode}:')
        for score in response:
            pp = round(score['pp'])
            beatmapset_artist = score['beatmapset']['artist']
            beatmapset_title = score['beatmapset']['title']
            beatmap_url = score['beatmap']['url']
            msg += f'{pp}pp on [{beatmapset_artist} - {beatmapset_title}]({beatmap_url})\n'
        embed.add_field(name='Scores', value=msg)
        await message.channel.send(embed=embed)
    elif message.content.startswith('!recent'):
        data = message.content.split()
        user = data[1]
        if len(data) > 2:
            if data[2] == 'ctb':
                response = get_recent_score(get_userid(user), mode='fruits')
            elif data[2] == 'taiko':
                response = get_recent_score(get_userid(user), mode='taiko')
            elif data[2] == 'mania':
                response = get_recent_score(get_userid(user), mode='mania')
            else:
                response = get_recent_score(get_userid(user), mode='osu')
        else:
            response = get_recent_score(get_userid(user))
        if len(response) == 0:
            await message.channel.send('No recent scores')
        else:
            response = response[0]
            player = response['user']['username']
            beatmap_artist = response['beatmapset']['artist']
            beatmap_name = response['beatmapset']['title']
            mode = response['mode']
            beatmap_link = response['beatmap']['url']
            if response['pp'] != None:
                pp = str(round(response['pp']))+'pp'
            else:
                pp = ''
            rank = response['rank']
            accuracy = str(round(response['accuracy']*100, 2))+'%'
            embed = discord.Embed(title=f'Recent score of {player} in {mode} is')
            embed.add_field(name='Song', value=f'[{beatmap_artist} - {beatmap_name}]({beatmap_link})')
            embed.add_field(name='Stats', value=f'{pp}\nRank: {rank}\nAccuracy: {accuracy}')
            await message.channel.send(embed=embed)
            print(response)
    elif message.content.startswith('!sus'):
        await message.channel.send('AMOGUS')
client.run(str(ds_token))