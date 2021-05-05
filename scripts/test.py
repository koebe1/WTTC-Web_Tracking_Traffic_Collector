import multiprocessing
from open_website_1 import call_website_1
from open_website_2 import call_website_2
from open_website_3 import call_website_3


def call_parallel(website_1, website_2, website_3):
    print("test")
    # call websites simultaneously
    # c1 = multiprocessing.Process(
    #     target=call_website_1, args=[website_1])
    # print("test2")
    # c2 = multiprocessing.Process(
    #     target=call_website_2, args=[website_2])
    # c3 = multiprocessing.Process(
    #     target=call_website_3, args=[website_3])

    print("test3")
    if __name__ == "__main__":
        print("test4")
        # c1.start()
        # c2.start()
        # c3.start()
        # c1.join()
        # c2.join()
        # c3.join


# call_parallel("https://example.com",
#               "https://example.com", "https://example.com")
