import requests

headers = {
    'authority': 'www.leovegas.es',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'accept': '*/*',
    'origin': 'https://www.leovegas.es',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.leovegas.es/es-es/apuestas-deportivas',
    'accept-language': 'es-ES,es;q=0.9',
    'cookie': '_gid=GA1.2.1301657150.1646599525; visid_incap_2121613=LqIIVeIJRTOo8LtpuvUGVGMdJWIAAAAAQUIPAAAAAACtWMc8xT7L0I3VDV2o0B61; incap_ses_506_2121613=XsAxMtJQxUCTeXkJ8KwFB2MdJWIAAAAAwQfyjNfd2bSE+rwfbLp97A==; _hjFirstSeen=1; _hjSession_380080=eyJpZCI6ImFhZTYwMDc4LWViNjgtNDU4MS05YTQ3LTk4NTkyNjE5Njk1MCIsImNyZWF0ZWQiOjE2NDY1OTk1MjUwMTgsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; data=2e98ded035acd011d0a5d23f80713692; leonrpid=3581232; leonrbid=1511; leonrmeta=[]; __qca=P0-132229501-1646599551424; _hjSessionUser_380080=eyJpZCI6IjI4YzEyNmQ5LTQ0M2QtNTAzNi1iMGZmLTRhM2I5MTVkZDI5NSIsImNyZWF0ZWQiOjE2NDY1OTk1MjUwMTAsImV4aXN0aW5nIjp0cnVlfQ==; _hjIncludedInSessionSample=0; _hjCachedUserAttributes=eyJhdHRyaWJ1dGVzIjp7InVzZXJfc2VnbWVudCI6IlVOS05PV05fTE9HR0VEX09VVCJ9LCJ1c2VySWQiOm51bGx9; FPID=FPID2.2.cYx11SgnFGR0TV8x29fRQpNp4ciX%2FDYqGnpxtWIRxuk%3D.1646599525; _gcl_au=1.1.903354475.1646599555; afUserId=78fb55a3-941c-42af-8805-6e48490b76e0-p; AF_SYNC=1646599555641; FPLC=zp0Oi4HQKoTFY7ZDY4mRpXUvmM%2FDy2afTaIAOb3HPyMXndKdPrktSUMvdu9mnqP4OtRnY%2B4BJkRaIfXVCuOKId5IX339K7dQloEzjJbPZd8AilzSwXhCpD6ler94%2BQ%3D%3D; s_fbp=fb.1.1646599554818.1296706856; leobtag=660140_B240A47ABEF446C2A4F98A33B1B7337A; leo_previous_page=https://www.leovegas.es/es-es/apuestas-deportivas; _ga=GA1.1.85756096.1646599525; _uetsid=6b6140c09d8e11ec8b55132b439ba2c1; _uetvid=6b625c509d8e11ecb79427e97a6c173f; _gat_leo=1; _ga_WDT7YBXB77=GS1.1.1646599554.1.1.1646599644.0',
}

json_data = {
    'query': 'query ListPageQuery(\n  $market: String!\n  $language: String!\n  $filter: FilterEventsByGroup\n) {\n  eventsByGroup(market: $market, language: $language, filter: $filter) {\n    results {\n      header\n      key\n      eventsSubGroup {\n        header\n        key\n        eventsSubGroup {\n          header\n          key\n          data {\n            id\n            englishName\n            awayName\n            homeName\n            type\n            sortOrder\n            start\n            state\n            sport\n            liveBoCount\n            liveBetOffers\n            nonLiveBoCount\n            streamsAvailable\n            mainBetHeaders\n            betOffers {\n              ...BetOffers_betOffers\n            }\n            liveData {\n              ...LiveData_liveData\n            }\n            path {\n              termKey\n              name\n            }\n            countryKey\n            country\n            groupKey\n            participants {\n              ...Participants_participants\n            }\n            tags\n          }\n          eventsSubGroup {\n            data {\n              id\n              englishName\n              awayName\n              homeName\n              type\n              sortOrder\n              start\n              state\n              sport\n              liveBoCount\n              liveBetOffers\n              nonLiveBoCount\n              streamsAvailable\n              mainBetHeaders\n              betOffers {\n                ...BetOffers_betOffers\n              }\n              liveData {\n                ...LiveData_liveData\n              }\n              path {\n                termKey\n                name\n              }\n              countryKey\n              country\n              groupKey\n              participants {\n                ...Participants_participants\n              }\n              tags\n            }\n          }\n        }\n      }\n    }\n    filterMeta {\n      matchCount\n      outrightCount\n    }\n    popularLeagues {\n      sport\n      popularGroups {\n        path\n      }\n    }\n  }\n}\n\nfragment BetOffers_betOffers on BetOffer {\n  id\n  main\n  mainLine\n  active\n  suspended\n  betOfferType {\n    id\n    name\n  }\n  eachWay {\n    terms\n  }\n  outcomes {\n    id\n    criterion {\n      type\n      name\n    }\n    distance\n    label\n    occurrence {\n      occurrenceType\n      occurrenceTypeLabel\n    }\n    odds\n    oddsFractional\n    oddsAmerican\n    scratched\n    status\n    type\n  }\n  scorerType {\n    type\n    name\n  }\n}\n\nfragment LiveData_liveData on LiveData {\n  eventId\n  matchClock {\n    ...MatchClock_matchClock\n  }\n  score {\n    ...Score_score\n  }\n  statistics {\n    __typename\n    ...Statistics_statistics\n  }\n  liveStatistics {\n    ...LiveStatistics_liveStatistics\n  }\n}\n\nfragment LiveStatistics_liveStatistics on LiveStatisticsOccurance {\n  occurrenceTypeId\n  count\n}\n\nfragment MatchClock_matchClock on MatchClock {\n  running\n  minute\n  second\n  minutesLeftInPeriod\n  secondsLeftInMinute\n  disabled\n  updatedAt\n}\n\nfragment Participants_participants on EventParticipant {\n  participantId\n  participantType\n  name\n}\n\nfragment Score_score on Score {\n  away\n  home\n  info\n}\n\nfragment Statistics_statistics on Statistics {\n  ... on TennisStatistics {\n    sets {\n      home\n      away\n      homeServe\n    }\n  }\n  ... on FootballStatistics {\n    football {\n      home {\n        yellowCards\n        redCards\n        corners\n      }\n      away {\n        yellowCards\n        redCards\n        corners\n      }\n    }\n  }\n}\n',
    'variables': {
        'market': 'ES',
        'language': 'es_ES',
        'filter': {
            'paths': [
                {
                    'path': 'tennis/all/all/all/in-play',
                },
            ],
            'attributes': [
                'matches',
            ],
            'groupBy': [
                'startDay',
                'groupId',
                'sport',
            ],
            'orderBy': [
                'start',
            ],
            'groupHeaders': [
                'startDay',
                'group',
            ],
            'useKambiPopularity': False,
            'timeStamp': '20220306T210000+01:00',
        },
    },
}

response = requests.post('https://www.leovegas.es/api/gql', headers=headers, json=json_data)


# URL visitada por el usuario:
# https://www.leovegas.es/es-es/apuestas-deportivas#filter/tennis