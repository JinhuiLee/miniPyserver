


def hello(verb, path, query):
    return "Server received your " + verb + " request" + str(query) + "\r\n"



def register(urlMapper):
    urlMapper["/hello"] = hello


    

    
    
        
