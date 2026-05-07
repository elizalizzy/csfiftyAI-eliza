import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    distribution = {}

    # number of pages linked
    n = len(corpus)

    # checking if links existeds in the first palce
    if corpus[page]:

        # random probability distiribution
        for p in corpus:
            distribution[p] = (1 - damping_factor) / n

        # probability distribution for linked pages
        for p in corpus[page]:
            distribution[p] += damping_factor / len(corpus[page])

    # if no lnks exist is the page
    else:
        # equal probabiltiy distibution
        for p in corpus:
            distribution[p] = 1 / n

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    PageRank = {}

    # keeps travk of the number of visits of to each page
    PageVisits = {page: 0 for page in corpus}

    # first page
    page = random.choice(list(corpus.keys()))

    for _ in range(n):

        # update page visits
        PageVisits[page] += 1

        # update the page tiself using transition model
        model = transition_model(corpus, page, damping_factor)

        page = random.choices(list(model.keys()), weights=model.values())[0]

    # calculate pagerank
    for p in PageVisits:
        PageRank[p] = PageVisits[p] / n

    return PageRank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
   # distribute probability
    PageRank = {page: 1 / len(corpus) for page in corpus}

    # convergence margin
    margin = 0.001

    # loop until the values converge
    while True:

        calculated_ranks = {}

        # distribute random probablitiy
        for page in corpus:
            calculated_ranks[page] = (1 - damping_factor) / len(corpus)

        # distribute and add linked pages probabilityies
        for page in corpus:
            # check if links ar epresent on the current page
            if corpus[page]:
                for p in corpus[page]:
                    calculated_ranks[p] += damping_factor * (PageRank[page] / len(corpus[page]))
            # if there are no links on th page
            else:
                for p in corpus:
                    calculated_ranks[p] += damping_factor * (PageRank[page] / len(corpus))
        # check margin
        if max(abs(calculated_ranks[p] - PageRank[p]) for p in PageRank) < margin:
            break

        PageRank = calculated_ranks

    return PageRank


if __name__ == "__main__":
    main()
