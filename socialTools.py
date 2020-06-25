# takes the inputted data and
# posts to the seperate socil media


def fbPost(text, image):
    # post data to facebook
    status = f"{text} {image}"
    return status


def twPost(text, image):
    # post data to twitter
    status = f"{text} {image}"
    return status


def inPost(text, image):
    # post data to instagram
    status = f"{text} {image}"
    return status


def allPost(text, image):
    fbPost(text, image)
    twPost(text, image)
    inPost(text, image)
