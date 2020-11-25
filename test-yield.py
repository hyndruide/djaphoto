

def f():
    print("toto 1")
    yield
    print("toto 2")

    return "toto 3"


def range(start, step):
    while True:
        new_start = yield start
        if new_start is not None:
            start = new_start
        else:
            start = start + step


def list_paragraph(fp):
    all_paragraphs = []
    paragraph = []

    for line in fp:
        line = line.rstrip()
        if line == "":
            value = "\n".join(paragraph)
            all_paragraphs.append(value)
            # process value
            paragraph = []
        
        else:
            paragraph.append(line)
       
    return all_paragraphs


def list_paragraph2(fp):
    paragraph = []
    
    for line in fp:
        line = line.rstrip()
        if line == "":
            value = "\n".join(paragraph)
            yield value
            # process value
            paragraph = []    
        else:
            paragraph.append(line)


with open("test-yield.py") as fp:
    for p in list_paragraph2(fp):
        print("mon paragraphe == {}".format(p))