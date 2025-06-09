
import sys
import bs4
import requests
import collections
import argparse
import urllib.parse
import pickle
import copy


def create_relative_urls_dictionary(args_list):
    """
    Creates a dictionary of relative urls based on a txt file.
    """
    relative_urls = args_list[3]
    traffic_dict = dict()
    with open(relative_urls) as relative_urls_text:
        for row in relative_urls_text:
            relative_url = row.rstrip()
            traffic_dict[relative_url] = dict()
    return traffic_dict


def get_html(base_url, relative_url):
    """
    Get html from real url.
    """
    full_url = urllib.parse.urljoin(base_url, relative_url)
    response = requests.get(full_url)
    html_of_relative_url = response.text
    return html_of_relative_url


def crawl(args_list):
    """
    Returns a dictionary that where each key is a relative URL that returns a dictionary which contains urls as keys
    and values that show how many links are there from the first relative url to the second one in the dictionary.
    """
    base_url = args_list[2]
    traffic_dict = create_relative_urls_dictionary(args_list)
    for relative_url in traffic_dict.keys():
        links_dict_count_for_relative_url = dict()
        temp_links = []
        html = get_html(base_url, relative_url)
        soup = bs4.BeautifulSoup(html, 'html.parser')
        for p in soup.find_all("p"):
            for link in p.find_all("a"):
                link = link.get("href")
                if link == "":
                    continue
                else:
                    links_dict_count_for_relative_url[link] = 0
                    temp_links.append(link)
        for link in traffic_dict.keys():
            relative_url_count = temp_links.count(link)
            if relative_url_count > 0:
                links_dict_count_for_relative_url[link] = relative_url_count
            elif relative_url_count == 0:
                # links_dict_count_for_relative_url[link] = 0
                continue
        copied = copy.deepcopy(links_dict_count_for_relative_url)
        for link in links_dict_count_for_relative_url.keys():
            if links_dict_count_for_relative_url[link] == 0:
                del copied[link]
        traffic_dict[relative_url] = copied

    return traffic_dict


def save_pickle(dict, args_list):
    """
    saves a file as a pickle type.
    """
    output_file_name = args_list[4]
    with open(output_file_name, 'wb') as f:
        pickle.dump(dict, f)


def calc_new_r(traffic_dict, r):
    """
    calculates the new values based on the formula given from part 2 and returns them as a dictionary.
    """
    new_r = dict()
    for key in traffic_dict.keys():
        new_r[key] = 0

    for new_r_url in new_r.keys():
        total = 0
        for key in traffic_dict.keys():
            dictionary = traffic_dict[key]
            if new_r_url not in dictionary:
                links_to_url_from_dict = 0
            else:
                links_to_url_from_dict = dictionary[new_r_url]
            sum_of_links = 0
            for value in dictionary.values():
                sum_of_links += value
            fraction = links_to_url_from_dict / sum_of_links
            total += r[key] * fraction
        new_r[new_r_url] = total
    return new_r


def page_rank(args_list):
    """
    Returns a dictionary with ranks for each relative url based on how many relative links point to it.
    """
    iterations = int(args_list[2])
    r = dict()
    dict_file_name = args_list[3]
    with open(dict_file_name, 'rb') as f:
        traffic_dict = pickle.load(f)
    for key in traffic_dict.keys():
        r[key] = 1
    if iterations == 0:
        return r

    for iteration in range(iterations):
        # initialize new_r with 0 values
        new_r = calc_new_r(traffic_dict, r)
        r = new_r
    return r


def create_empty_relative_urls_dictionary(args_list):
    """
    Creates a dictionary with relative urls as keys and no values.
    """
    links_dictionary = create_relative_urls_dictionary(args_list)
    for key in links_dictionary.keys():
        links_dictionary[key] = None
    return links_dictionary


def words_dict(args_list):
    """
    Returns a word dictionary that shows for each word scanned from the html links, how many times it is written in
    each relative url.
    """
    base_url = args_list[2]
    links_dictionary = create_empty_relative_urls_dictionary(args_list)
    words_dictionary = dict()
    for relative_url in links_dictionary.keys():
        html = get_html(base_url, relative_url)
        soup = bs4.BeautifulSoup(html, 'html.parser')
        for p in soup.find_all("p"):
            content = p.text
            content = content.split()
            for i in range(len(content)):
                stripped = (content[i]).rstrip()
                content[i] = stripped
            for word in content:
                if word in words_dictionary:
                    if relative_url in words_dictionary[word]:
                        words_dictionary[word][relative_url] += 1
                    else:
                        words_dictionary[word][relative_url] = 1
                else:
                    relative_url_dictionary = dict()
                    relative_url_dictionary[relative_url] = 1
                    words_dictionary[word] = (relative_url_dictionary)

    copied = copy.deepcopy(words_dictionary)
    for key in words_dictionary.keys():
        for link_key in words_dictionary[key].keys():
            if words_dictionary[key][link_key] is None or words_dictionary[key][link_key] == 0:
                del copied[key][link_key]

    return copied


def load_pickle_file(file_path):
    """
    Loads a pickle file.
    """
    with open(file_path, 'rb') as f:
        d = pickle.load(f)
    return d


def search(args_list):
    """
    Returns a dictionary with relative urls and their rank based on a special formula and arguments given by the user.
    """
    query = args_list[2]
    query_words_list = query.split()
    ranking_dictionary = load_pickle_file(args_list[3])
    words_dictionary = load_pickle_file(args_list[4])
    max_results = args_list[5]

    for i in range(len(query_words_list) - 1, -1, -1):
        if query_words_list[i] in words_dictionary:
            continue
        else:
            query_words_list.pop(i)

    if len(query_words_list) == 0:
        return None

    relative_urls_to_rank = []
    for relative_url in ranking_dictionary.keys():
        relative_urls_to_rank.append(relative_url)

    for word in query_words_list:
        for relative_url in ranking_dictionary.keys():
            if relative_url not in words_dictionary[word]:
                relative_urls_to_rank.remove(relative_url)
            else:
                continue

    rank_and_page = []
    for relative_url in relative_urls_to_rank:
        Y = ranking_dictionary[relative_url]
        rank_and_page.append((Y, relative_url))

    rank_and_page.sort(reverse=True)
    if len(rank_and_page) > int(max_results):
        rank_and_page_max = rank_and_page[:int(max_results)]
    else:
        rank_and_page_max = rank_and_page

    relative_urls_to_rank = []
    for tuple in rank_and_page_max:
        Y, relative_url = tuple
        relative_urls_to_rank.append(relative_url)

    relative_urls_scored = []
    for relative_url in relative_urls_to_rank:
        Y = ranking_dictionary[relative_url]
        all_z = []
        for word in query_words_list:
            Z = words_dictionary[word][relative_url]
            all_z.append(Z)
        all_z.sort()
        relative_url_score = Y * all_z[0]
        relative_urls_scored.append((relative_url_score, relative_url))

    relative_urls_scored.sort(reverse=True)

    for object in relative_urls_scored:
        score, page = object
        line = str(page) + " " + str(score) + "\n"
        create_text_file(line)

        print(page, score)
    create_text_file("*" * 10)
    create_text_file("\n")


def create_text_file(line):
    with open('results.txt', 'a') as f:
        f.write(line)
    return f


def main():
    args_list = sys.argv

    if args_list[1] == "crawl":
        traffic_dict = crawl(args_list)
        save_pickle(traffic_dict, args_list)

    elif args_list[1] == "page_rank":
        r = page_rank(args_list)
        save_pickle(r, args_list)

    elif args_list[1] == "words_dict":
        words_dictionary = words_dict(args_list)
        save_pickle(words_dictionary, args_list)

    elif args_list[1] == "search":
        search(args_list)


if __name__ == '__main__':
    main()
