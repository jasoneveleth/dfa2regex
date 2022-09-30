from subprocess import run, PIPE, Popen, DEVNULL

result = run(['python', 'hi.py'], stdout=PIPE)
result = result.stdout.decode('utf-8')

paragraph = ""
for line in result.split('\n'):
    if line == "":
        # save and reset paragraph
        output = bytes(paragraph[:-1], 'utf-8')
        paragraph = ""

        colors = ['-Gbgcolor=transparent', 
                '-Gcolor=#abb2bf', 
                '-Gfontcolor=#abb2bf', 
                '-Gfontname=Hack', 
                '-Grankdir=LR', 
                '-Nfontname=Hack', 
                '-Nfontcolor=#abb2bf', 
                '-Ncolor=#abb2bf', 
                '-Efontcolor=#abb2bf', 
                '-Efontname=Hack', 
                '-Ecolor=#abb2bf']
        cmd1 = ['dot', '-Tsvg', *colors]
        cmd2 = ['rsvg-convert', '--zoom=3']
        cmd3 = ['kitty', '+kitten', 'icat', '--align=left']

        for cmd in [cmd1, cmd2, cmd3]:
            pipe = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=DEVNULL)
            output = pipe.communicate(input=output)[0]

        print(output)
    else:
        paragraph += line + '\n'
