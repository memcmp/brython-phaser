from browser import document, alert


def echo(ev):
    alert(document["zone"].value)


document['mybutton'].bind('click', echo)
