#Flask Watch it
from flask import Flask, request, url_for, send_file, render_template, make_response
from datetime import datetime
import pickle
import math
import requests
from search_torrent import search_torrent_file_galaxy, search_torrent_file_1337x, search_torrent_file_torrentdownload_dot_info, search_torrent_magnet_galaxy, search_torrent_magnet_1337x, search_torrent_magnet_torrentdownload_dot_info, search_torrent_file_limetorrents

app = Flask(__name__)

supported_languages = [
    'bi', 'cs', 'ba', 'ae', 'av', 'de', 'mt', 'om', 'rm', 'so', 'ts', 'vi',
    'gn', 'ig', 'it', 'ki', 'k', 'la', 'ln', 'lb', 'ny', 'pl', 'si', 'to',
    'az', 'ce', 'c', 'da', 'hz', 'ie', 'rw', 'mi', 'no', 'pi', 'sk', 'se',
    'sm', 'uk', 'en', 'ay', 'ca', 'eo', 'ha', 'ho', 'h', 'io', 'ii', 'kn',
    'kv', 'li', 'oj', 'r', 'sr', 'sv', 'ty', 'z', 'ka', 'ch', 'be', 'br', 'kw',
    'fi', 'sh', 'nn', 'tt', 'tg', 'vo', 'ps', 'mk', 'fr', 'bm', 'e', 'fj',
    'id', 'mg', 'na', 'xx', 'q', 'sq', 'ti', 'tw', 'wa', 'ab', 'bs', 'af',
    'an', 'fy', 'g', 'ik', 'ja', 'ko', 'lg', 'nl', 'os', 'el', 'bn', 'cr',
    'km', 'lo', 'nd', 'ne', 'sc', 'sw', 'tl', 'ur', 'ee', 'aa', 'co', 'et',
    'is', 'ks', 'kr', 'ky', 'kj', 'nr', 'or', 'wo', 'za', 'ar', 'cv', 'fo',
    'hr', 'ms', 'nb', 'rn', 'sn', 'st', 'tr', 'am', 'fa', 'hy', 'pa', 'as',
    'ia', 'lv', 'l', 'mr', 'mn', 'pt', 'th', 'tk', 've', 'dv', 'gv', 'kl',
    'kk', 'lt', 'my', 'sl', 'sd', 'cn', 'hi', 'cy', 'ht', 'i', 'jv', 'mh',
    'sa', 'ss', 'te', 'kg', 'ml', 'uz', 'sg', 'xh', 'es', 's', 'ug', 'yi',
    'yo', 'zh', 'he', 'bo', 'ak', 'mo', 'ng', 'dz', 'ff', 'gd', 'ga', 'gl',
    'nv', 'oc', 'ro', 'ta', 'tn', 'bg'
]
rtl_languages = [
    'ar', 'dv', 'fa', 'ha', 'he', 'ks', 'ku', 'ps', 'sd', 'ur', 'yi'
]
with open('dict_translate.pkl', 'rb') as dict_translate_pkl:
    dict_translate = pickle.load(dict_translate_pkl)


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


@app.route("/")
def main_page():
    lang = request.cookies.get('lang')
    if (lang == None):
        lang = request.accept_languages.best_match(supported_languages)
    if (lang == None):
        lang = "en"
    resp = make_response(
        render_template('main.html',
                        main_active=True,
                        content=get_main_page_content(lang=lang),
                        Home=dict_translate[lang]['Home'],
                        Movies=dict_translate[lang]['Movies'],
                        TV_Shows=dict_translate[lang]['TV Shows'],
                        Actors=dict_translate[lang]['Actors'],
                        Search=dict_translate[lang]['Search'],
                        is_rtl=(lang in rtl_languages)))
    return resp


@app.route("/Movie/<id>")
def movie_page(id):
    lang = request.cookies.get('lang')
    if (lang == None):
        lang = request.accept_languages.best_match(supported_languages)
    if (lang == None):
        lang = "en"
    (imdbid, title, original_title, overview, generes_list, rating,
     release_date, runtime, poster_url, backdrop_url, number_of_seasons,
     number_of_episodes, seasons_name, seasons_nunmber,
     episode_per_season) = get_movie_details(id, lang=lang)
    return render_template(
        'movie.html',
        imdbid=imdbid,
        id=id,
        title=title,
        original_title=original_title,
        overview=overview,
        generes_list=generes_list,
        rating=rating,
        release_date=release_date,
        runtime=runtime,
        poster_url=poster_url,
        backdrop_url=backdrop_url,
        Home=dict_translate[lang]['Home'],
        Movies=dict_translate[lang]['Movies'],
        TV_Shows=dict_translate[lang]['TV Shows'],
        Actors=dict_translate[lang]['Actors'],
        Search=dict_translate[lang]['Search'],
        Original_Title=dict_translate[lang]['Original Title'],
        Categories=dict_translate[lang]['Categories'],
        Time=dict_translate[lang]['Time'],
        Minutes=dict_translate[lang]['Minutes'],
        Release_Date=dict_translate[lang]['Release Date'],
        Play_Video=dict_translate[lang]['Play Video'],
        is_rtl=(lang in rtl_languages))


@app.route("/TV_Show/<id>")
def tv_page(id):
    lang = request.cookies.get('lang')
    if (lang == None):
        lang = request.accept_languages.best_match(supported_languages)
    if (lang == None):
        lang = "en"
    (imdbid, title, original_title, overview, generes_list, rating,
     release_date, runtime, poster_url, backdrop_url, number_of_seasons,
     number_of_episodes, seasons_name, seasons_nunmber,
     episode_per_season) = get_tv_show_details(id, lang=lang)
    return render_template(
        'tv_show.html',
        title=title,
        original_title=original_title,
        overview=overview,
        generes_list=generes_list,
        rating=rating,
        release_date=release_date,
        runtime=runtime,
        poster_url=poster_url,
        backdrop_url=backdrop_url,
        number_of_seasons=number_of_seasons,
        number_of_episodes=number_of_episodes,
        seasons_name=seasons_name,
        seasons_nunmber=seasons_nunmber,
        episode_per_season=episode_per_season,
        Home=dict_translate[lang]['Home'],
        Movies=dict_translate[lang]['Movies'],
        TV_Shows=dict_translate[lang]['TV Shows'],
        Actors=dict_translate[lang]['Actors'],
        Search=dict_translate[lang]['Search'],
        Original_Title=dict_translate[lang]['Original Title'],
        Categories=dict_translate[lang]['Categories'],
        Number_Of_Seasons=dict_translate[lang]['Number Of Seasons'],
        Number_Of_Episodes=dict_translate[lang]['Number Of Episodes'],
        Episode_Time=dict_translate[lang]['Episode Time'],
        Minutes=dict_translate[lang]['Minutes'],
        First_Air_Date=dict_translate[lang]['First Air Date'],
        Choose_Season=dict_translate[lang]['Choose Season'],
        Choose_Episode=dict_translate[lang]['Choose Episode'],
        Play_Video=dict_translate[lang]['Play Video'],
        is_rtl=(lang in rtl_languages))


@app.route("/Person/<id>")
def person_page(id):
    lang = request.cookies.get('lang')
    if (lang == None):
        lang = request.accept_languages.best_match(supported_languages)
    if (lang == None):
        lang = "en"
    (name, also_known_as, biography, popularity, birthday, deathday,
     known_for_department, place_of_birth, poster_url, known_for_items,
     backdrop_url) = get_person_details(id, lang=lang)
    return render_template(
        'person.html',
        name=name,
        also_known_as=also_known_as,
        biography=biography,
        popularity=popularity,
        birthday=birthday,
        deathday=deathday,
        known_for_department=known_for_department,
        place_of_birth=place_of_birth,
        poster_url=poster_url,
        known_for_items=known_for_items,
        backdrop_url=backdrop_url,
        Home=dict_translate[lang]['Home'],
        Movies=dict_translate[lang]['Movies'],
        TV_Shows=dict_translate[lang]['TV Shows'],
        Actors=dict_translate[lang]['Actors'],
        Search=dict_translate[lang]['Search'],
        Also_Known_As=dict_translate[lang]['Also Known As'],
        Birth_Date=dict_translate[lang]['Birth Date'],
        Place_Of_Birth=dict_translate[lang]['Place Of Birth'],
        Known_For_Department=dict_translate[lang]['Known For Department'],
        Popularity=dict_translate[lang]['Popularity'],
        is_rtl=(lang in rtl_languages))


import cloudscraper


#@app.route("/get_torrent/<id>")
#@app.route("/get_torrent/<id>/<e_id>")
@app.route("/get_torrent/<q>")
@app.route("/get_torrent/<q>/<magnet>")
def get_torrent(q, magnet=None):
    print("q,magnet",q,magnet)
    if (magnet):
        magnet_link = search_torrent_magnet_galaxy(q)
        if (magnet_link == ""):
            magnet_link = search_torrent_magnet_torrentdownload_dot_info(q)
        if (magnet_link == ""):
            magnet_link = search_torrent_magnet_1337x(q)
        return magnet_link
    else:
        torrent_file = search_torrent_file_galaxy(q)
        if (torrent_file == ""):
            torrent_file = search_torrent_file_torrentdownload_dot_info(q)
        if (torrent_file == ""):
            torrent_file = search_torrent_file_1337x(q)
        if (torrent_file == ""):
            torrent_file = search_torrent_file_limetorrents(q)
        '''
        if not (torrent_file == ""):
            return send_file(io.BytesIO(torrent_file),
                             attachment_filename='torrent_file.torrent',
                             mimetype='application/x-bittorrent')
        return ""
        '''
        return torrent_file


@app.route("/get_lang")
def get_lang():
    lang = request.cookies.get('lang')
    if (lang == None):
        lang = request.accept_languages.best_match(supported_languages)
    if (lang == None):
        lang = "en"
    return lang


@app.route("/get_imdb/<id>/<se>/<ep>")
def get_imdb(id, se, ep):
    return get_tv_show_imdb(id, se, ep)


@app.route("/TV_Shows")
@app.route("/TV_Shows/<page>")
def tv_shows_page(page=1):
    lang = request.cookies.get('lang')
    if (lang == None):
        lang = request.accept_languages.best_match(supported_languages)
    if (lang == None):
        lang = "en"
    if page == 1:
        resp = make_response(
            render_template('items_list.html',
                            tv_shows_active=True,
                            items=get_trending_tv_shows(page,
                                                        "/w500",
                                                        lang=lang),
                            Home=dict_translate[lang]['Home'],
                            Movies=dict_translate[lang]['Movies'],
                            TV_Shows=dict_translate[lang]['TV Shows'],
                            Actors=dict_translate[lang]['Actors'],
                            Search=dict_translate[lang]['Search'],
                            is_rtl=(lang in rtl_languages)))
        return resp
    return render_template(
        'items_ajax.html',
        items=get_trending_tv_shows(page, "/w500", lang=lang),
    )


@app.route("/Movies")
@app.route("/Movies/<page>")
def movies_page(page=1):
    lang = request.cookies.get('lang')
    if (lang == None):
        lang = request.accept_languages.best_match(supported_languages)
    if (lang == None):
        lang = "en"
    if page == 1:
        resp = make_response(
            render_template('items_list.html',
                            movies_active=True,
                            items=get_trending_movies(page, "/w500",
                                                      lang=lang),
                            Home=dict_translate[lang]['Home'],
                            Movies=dict_translate[lang]['Movies'],
                            TV_Shows=dict_translate[lang]['TV Shows'],
                            Actors=dict_translate[lang]['Actors'],
                            Search=dict_translate[lang]['Search'],
                            is_rtl=(lang in rtl_languages)))
        return resp
    return render_template(
        'items_ajax.html',
        items=get_trending_movies(page, "/w500", lang=lang),
    )


@app.route("/Persons")
@app.route("/Persons/<page>")
def persons_page(page=1):
    lang = request.cookies.get('lang')
    if (lang == None):
        lang = request.accept_languages.best_match(supported_languages)
    if (lang == None):
        lang = "en"
    if page == 1:
        resp = make_response(
            render_template('items_list.html',
                            persons_active=True,
                            items=get_popular_persons(page, "/w500",
                                                      lang=lang),
                            Home=dict_translate[lang]['Home'],
                            Movies=dict_translate[lang]['Movies'],
                            TV_Shows=dict_translate[lang]['TV Shows'],
                            Actors=dict_translate[lang]['Actors'],
                            Search=dict_translate[lang]['Search'],
                            is_rtl=(lang in rtl_languages)))
        return resp
    return render_template(
        'items_ajax.html',
        items=get_popular_persons(page, "/w500", lang=lang),
    )


@app.route("/Search/<q>")
@app.route("/Search/<q>/<page>")
def search_page(q, page=1):
    lang = request.cookies.get('lang')
    if (lang == None):
        lang = request.accept_languages.best_match(supported_languages)
    if (lang == None):
        lang = "en"
    if page == 1:
        resp = make_response(
            render_template('items_list.html',
                            movies_active=True,
                            items=get_search(page, q, "/w500", lang=lang),
                            Home=dict_translate[lang]['Home'],
                            Movies=dict_translate[lang]['Movies'],
                            TV_Shows=dict_translate[lang]['TV Shows'],
                            Actors=dict_translate[lang]['Actors'],
                            Search=dict_translate[lang]['Search'],
                            is_rtl=(lang in rtl_languages)))
        return resp
    return render_template(
        'items_ajax.html',
        items=get_search(page, q, "/w500", lang=lang),
    )


""" TMDB functions """
API_KEY = "4f2917841238275498913fb9c85b266f"

baseURL = "https://api.themoviedb.org/3"
image_url = "https://image.tmdb.org/t/p"

url_search = "/search/multi"

url_weeklytrendingMovies = "/trending/movie/week"
url_weeklytrendingShows = "/trending/tv/week"
url_topRatedMovies = "/movie/top_rated"
url_topRatedShows = "/tv/top_rated"
url_popularMovies = "/movie/popular"
url_popularShows = "/tv/popular"
url_popularPersons = "/person/popular"

url_movie_details = "/movie/"
url_tv_show_details = "/tv/"
url_season_details = "/season/"
url_episode_details = "/episode/"
url_person_details = "/person/"
url_person_credits_details = "/combined_credits"
url_external_ids = "/external_ids"


def get_main_page_content(lang="en"):
    content = []
    content.append((dict_translate[lang]["Weekly Trending TV Shows"],
                    get_trending_tv_shows(1, lang=lang)))
    content.append((dict_translate[lang]["Weekly Trending Movies"],
                    get_trending_movies(1, lang=lang)))
    content.append((dict_translate[lang]["Top Rated TV Shows"],
                    get_top_rated_tv_shows(1, lang=lang)))
    content.append((dict_translate[lang]["Top Rated Movies"],
                    get_top_rated_movies(1, lang=lang)))
    #content.append((dict_translate[lang]["Popular TV Shows"],get_popular_tv_shows(1, lang=lang)))
    #content.append((dict_translate[lang]["Popular Movies"],get_popular_movies(1, lang=lang)))
    return content


def get_item_list(query,
                  image_width,
                  image_type=None,
                  redirect_to=None,
                  is_add_backdrop=None):
    response = requests.get(query)
    if response.status_code == 200:
        #status code ==200 indicates the API query was successful
        data = response.json()

        item_list = []
        results = data["cast"] if "cast" in data else data["results"]
        for result in results:
            #if (result['media_type'] == 'movie'):
            item_list.append(
                (url_for(redirect_to if redirect_to else
                         (result['media_type'] + "_page"),
                         id=result['id']), image_url + image_width +
                 str(result[image_type if image_type else
                            ('poster_path' if 'poster_path' in
                             result else 'profile_path')]),
                 int(result['vote_average'] * 10) if 'vote_average' in result
                 else math.ceil(result['popularity']),
                 result['title'] if 'title' in result else result['name'],
                 ((result['overview'][:128] +
                   '....') if len(result['overview']) > 128 else
                  result['overview']) if 'overview' in result else ""))
        return ((item_list,
                 image_url + "/w1280" + results[0]["backdrop_path"]) if
                (is_add_backdrop and len(results)
                 and "backdrop_path" in results[0]) else item_list)
    else:
        return (None)


def get_item_details(query, big_poster_width, backdrop_width,
                     small_poster_width):
    response = requests.get(query)
    if response.status_code == 200:
        #status code ==200 indicates the API query was successful
        result = response.json()

        return (
            result['imdb_id'] if 'imdb_id' in result else "",
            result['title'] if 'title' in result else result['name'],
            result['original_title']
            if 'original_title' in result else result['original_name'],
            result['overview'] if 'overview' in result else "",
            [genere["name"]
             for genere in result['genres']] if "genres" in result else "",
            int(result['vote_average'] *
                10) if "vote_average" in result else "", result["release_date"]
            if "release_date" in result else result["first_air_date"],
            result["runtime"] if "runtime" in result else
            (result["episode_run_time"][0] if "episode_run_time" in result
             and len(result["episode_run_time"]) else ""),
            (image_url + big_poster_width +
             str(result["poster_path"])) if "poster_path" in result else "",
            (image_url + backdrop_width + str(result["backdrop_path"]))
            if "backdrop_path" in result else "", result["number_of_seasons"]
            if "number_of_seasons" in result else None,
            result["number_of_episodes"]
            if "number_of_episodes" in result else None,
            [str(season["name"])
             for season in result["seasons"]] if "seasons" in result else None,
            [str(season["season_number"])
             for season in result["seasons"]] if "seasons" in result else None,
            [(str(season["episode_count"]) if "episode_count" in season else 0)
             for season in result["seasons"]] if "seasons" in result else None)
    else:
        return (None)


def get_search(page, q, width="/w200", lang="en"):
    query = baseURL + url_search + "?api_key=" + API_KEY + "&language=" + lang + "&page=" + str(
        page) + "&include_adult=false" + "&query=" + q
    return get_item_list(query, width)


def get_trending_tv_shows(page, width="/w200", lang="en"):
    query = baseURL + url_weeklytrendingShows + "?api_key=" + API_KEY + "&language=" + lang + "&page=" + str(
        page)
    return get_item_list(query, width, 'poster_path', 'tv_page')


def get_trending_movies(page, width="/w200", lang="en"):
    query = baseURL + url_weeklytrendingMovies + "?api_key=" + API_KEY + "&language=" + lang + "&page=" + str(
        page)
    return get_item_list(query, width, 'poster_path', 'movie_page')


def get_top_rated_tv_shows(page, lang="en"):
    query = baseURL + url_topRatedShows + "?api_key=" + API_KEY + "&language=" + lang + "&page=" + str(
        page)
    return get_item_list(query, "/w200", 'poster_path', 'tv_page')


def get_top_rated_movies(page, lang="en"):
    query = baseURL + url_topRatedMovies + "?api_key=" + API_KEY + "&language=" + lang + "&page=" + str(
        page)
    return get_item_list(query, "/w200", 'poster_path', 'movie_page')


def get_popular_tv_shows(page, lang="en"):
    query = baseURL + url_popularShows + "?api_key=" + API_KEY + "&language=" + lang + "&page=" + str(
        page)
    return get_item_list(query, "/w200", 'poster_path', 'tv_page')


def get_popular_movies(page, lang="en"):
    query = baseURL + url_popularMovies + "?api_key=" + API_KEY + "&language=" + lang + "&page=" + str(
        page)
    return get_item_list(query, "/w200", 'poster_path', 'movie_page')


def get_popular_persons(page, width="/w200", lang="en"):
    query = baseURL + url_popularPersons + "?api_key=" + API_KEY + "&language=" + lang + "&page=" + str(
        page)
    return get_item_list(query, width, 'profile_path', 'person_page')


def get_movie_details(id, lang="en"):
    query = baseURL + url_movie_details + id + "?api_key=" + API_KEY + "&language=" + lang
    return get_item_details(query, "/w300", '/w1280', None)


def get_tv_show_details(id, lang="en"):
    query = baseURL + url_tv_show_details + id + "?api_key=" + API_KEY + "&language=" + lang
    return get_item_details(query, "/w300", '/w1280', "/w200")


def get_person_details(id, lang="en"):
    query = baseURL + url_person_details + id + url_person_credits_details + "?api_key=" + API_KEY + "&language=" + lang
    known_for_items, backdrop = get_item_list(query,
                                              "/w200",
                                              'poster_path',
                                              is_add_backdrop=True)

    query = baseURL + url_person_details + id + "?api_key=" + API_KEY + "&language=" + lang
    response = requests.get(query)
    if response.status_code == 200:
        result = response.json()

        return (result['name'] if 'name' in result else "",
                result['also_known_as'] if 'also_known_as' in result else "",
                result['biography'] if 'biography' in result else "",
                result['popularity'] if "popularity" in result else "",
                result["birthday"] if "birthday" in result else "",
                result["deathday"] if "deathday" in result else "",
                result["known_for_department"]
                if "known_for_department" in result else "",
                result["place_of_birth"] if "place_of_birth" in result else "",
                (image_url + "/w300" +
                 result["profile_path"]) if "profile_path" in result else "",
                known_for_items, backdrop)
    else:
        return (None)


def get_tv_show_imdb(id, se, ep):
    query = baseURL + url_tv_show_details + id + url_season_details + se + url_episode_details + ep + url_external_ids + "?api_key=" + API_KEY
    response = requests.get(query)
    if response.status_code == 200:
        #status code ==200 indicates the API query was successful
        result = response.json()
        return result['imdb_id'] if 'imdb_id' in result else ""
    else:
        return ""
