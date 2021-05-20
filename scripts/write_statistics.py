import os.path
import json
import paths

# Format of the parsed document
#
# +1
# ||adobedtm.com^$3p,domain=~adobe.com
# --
# www.spiegel.de
# 3
# script
# https://assets.adobedtm.com/cc10f7b4369d/cb3b620b1166/af1da404b6f7/RC862020349d4e4d60bfa847eb35924fc7-source.min.js


def write_statistic(curr_dir, sub_dir):

    captured = paths.captured

    json_file = os.path.join(captured, curr_dir, sub_dir, "data.json")

    def extract_url_app():
        total_blocked_urls_app = 0
        blocked_urls_app = []

        with open(json_file, 'r+') as file:
            # Transforms json input to python objects
            data = json.load(file)

        for packet in data:
            # check in packets labeled as tracker by app
            if "true" in packet["tracker"]:
                # count blocked urls by app
                total_blocked_urls_app += 1

                # get urls from http2 layer
                if "http2.header.value.url" in packet:
                    blocked_urls_app.append(packet["http2.header.value.url"])

                # get urls from http layer
                elif "http" in packet["_source"]["layers"]:
                    http = packet["_source"]["layers"]["http"]

                    if "http.request.full_uri" in http:
                        http_request_full_uri = packet["_source"]["layers"]["http"]["http.request.full_uri"]
                        blocked_urls_app.append(http_request_full_uri)

        return total_blocked_urls_app, blocked_urls_app

    d = extract_url_app()

    total_blocked_urls_app = d[0]
    blocked_urls_app = d[1]

    # print(total_blocked_urls_app)
    # print(total_blocked_both)
    # # print(blocked_both)

    def statistics():

        # statistcis sub_dir
        # f = open(os.path.join(captured, curr_dir,
        #          sub_dir, "statistics.txt"), "w+")
        # f.write(
        #     f"Anzahl Tracker-belasteter Datenpakete: Applikation: {total_blocked_urls_app}")

        h = open(os.path.join(captured, curr_dir, sub_dir,
                 "blocked_urls_application.txt"), "w+")

        h.write(f"URLS blocked by Application:  {total_blocked_urls_app}")
        h.write('\n' '\n')

        for row in blocked_urls_app:
            h.write(row + '\n' '\n')

    statistics()
    return total_blocked_urls_app


# extraced blocked urls by ublock
def extract_url_ublock(curr_dir, sub_dir):

    captured = paths.captured

    ublock_log = os.path.join(captured, curr_dir,  "ublock_log.txt")

    total_blocked_urls_uBlock = 0
    blocked_urls_ublock = []

    with open(ublock_log, 'r') as f:
        content = f.read().splitlines()

    # get index of the blocked sign "--" -> Url is always 4 entrys after "--"
    index = []
    for i, j in enumerate(content):
        if j == '--':
            index.append(i)

    for i in index:
        blocked_urls_ublock.append(content[i+4])
        total_blocked_urls_uBlock += 1

    # create and write to file

    # d = open(os.path.join(captured, curr_dir, sub_dir,
    #          "blocked_urls_ublock.txt"), "w+")

    # for row in blocked_urls_ublock:
    #     d.write(row + '\n' '\n')

    return total_blocked_urls_uBlock, blocked_urls_ublock
