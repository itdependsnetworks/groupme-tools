import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import json
import datetime
import os
from urlparse import urlparse

"""
Run Code by using the following:
python complex-transcript.py transcript-GROUP_ID.json  > FILENAME.html

Then Grep the files into a shell script (until I integrate the download)
grep 'input type=hidden' FILENAME.html| sed -e 's/<input type=hidden value="\(.*\)">/\1/' > shcurl.sh

Download the files
sh shcurl.sh
"""

def printTranscript(messages):
    """Prints a readable "transcript" from the given list of messages.

    Assumes the input list is sorted."""

    message_count ={}
    id_lookup = {}
    fav_got_total = {}
    fav_give_total = {}
    fav_matrix = {}
    user_count_total = {}
    user_count_avg = {}
    avatar_lines = {}
    total_count = 0
    like_total = 0
    name_change =[]
    group_change =[]
    avatar_change =[]
    comment_table = []
    pic_lines = []


    for message in messages:
        name = message[u'name']
        if message[u'user_id'] is not None:
            user_id = message[u'user_id']
        else:
            user_id = ''

        if name is not None and user_id is not None:
            id_lookup[user_id] = name
        else:
            user_id = ''

    for message in messages:
        name = message[u'name']


        time = datetime.datetime.fromtimestamp(message[u'created_at']).strftime('%Y-%m-%d %H:%M')

        # text is None for a photo message
        if message[u'text'] is not None:
            text = message[u'text']
        else:
            text = "(no text)"

        if message[u'user_id'] is not None and message[u'user_id'] != 'system':
            user_id1 = message[u'user_id']
            total_count += 1
            try:
                message_count[user_id1]
                tempcount = message_count[user_id1]
                tempcount += 1
                message_count[user_id1] = tempcount
            except:
                message_count[user_id1] = 1
        else:
                user_id1 = ''
                if message[u'text'] is not None:
                    msg = message[u'text']
                    if msg.find("changed name to") == -1:
                        print ""
                    else:
                        name_change.append(msg)
                    if msg.find("changed the group's name") == -1:
                        print ""
                    else:
                        group_change.append(msg)
                    if msg.find("changed the group's avatar") == -1:
                        print ""
                    else:
                        avatar_change.append(msg)


  

        if message[u'avatar_url'] is not None:
            #avatar = '<img src="' + message[u'avatar_url'] + '" height="42" width="42" ></img>'

            avatar_url = message[u'avatar_url']
            avatar_fileName = os.path.split(urlparse(avatar_url)[2])[1]

            a_curl = 'test -e img/' + avatar_fileName + '&& echo "File exists skip" || curl -o img/' + avatar_fileName + ' ' + avatar_url

            if avatar_fileName not in avatar_lines:
                avatar_lines[avatar_fileName] = a_curl
            #avatar = '<img src="' + message[u'avatar_url'] + '" height="42" width="42" ></img>'
            avatar = '<img src="img/' + avatar_fileName + '" height="42" width="42" ></img>'

        else:
            avatar = "(no pic)"


        if message[u'system'] is True:
            system_padded = '(SYS) '
        else:
            system_padded = ''

        if len(message[u'favorited_by']) is not 0:
            favorites_padded = ''
            fav_list = message[u'favorited_by']
            for auser in fav_list:
                favorites_padded += '<img src=img/heart.png alt ="' + str(id_lookup[auser]) + '" title="' + str(id_lookup[auser]) +'">'
                like_total += 1
                if user_id1 == 'system' or user_id1 is 0 or not user_id1:
                    test = ''
                elif user_id1 in fav_got_total:
                    fav_got_total[user_id1] += 1
                else:
                    fav_got_total[user_id1] = 1
                if auser in fav_give_total:
                    fav_give_total[auser] += 1
                else:
                    fav_give_total[auser] = 1

                combine = user_id1 + '-' + auser
                if user_id1 == 'system' or user_id1 is 0 or not user_id1:
                    test = ''
                elif combine in fav_matrix:
                    fav_matrix[combine] += 1
                else:
                    fav_matrix[combine] = 1
        else:
            favorites_padded = ''

        if message[u'picture_url'] is not None:
            url = message[u'picture_url']
            #pic = ' ; photo URL ' + url
            
            fileName = os.path.split(urlparse(url)[2])[1]
            curl = 'test -e img/' + fileName + '&& echo "File exists skip" || curl -o img/' + fileName + ' ' + url
            pic_lines.append(curl)
            pic = '<br><img src="img/' + fileName + '" height="400" width="300">'
        else:
            pic = ''

        line = '<tr class="a"><td class="a" rowspan="2">' + system_padded + avatar + '</td> <td class="a"> <span style="font-size:80%;color:darkgrey" title="' + time + '">' + name + '</span>' + favorites_padded + '</td></tr><tr class="a"><td class="a">' + text + pic + '</td></tr>'

        comment_table.append(line)

    for user_id2 in message_count:
        user_name = id_lookup[user_id2]
        average = ( float(message_count[user_id2]) / float(total_count) ) * 100
        user_count_total[user_id2] = message_count[user_id2]
        user_count_avg[user_id2] = int(average)

        #print user_name + ' Has created ' + str(message_count[user_id2]) + ' (%' + str(int(average)) + ') of ' + str(total_count) + '<br>'

    print '<br>'
    for name_change_line in name_change:
        print name_change_line + '<br>'
    print '<br>'
    for group_change_line in group_change:
        print group_change_line + '<br>'
    print '<br>'
    for avatar_change_line in avatar_change:
        print avatar_change_line + '<br>'
    print '<br>'
    #for fav_got_total_line in fav_got_total:
        #print id_lookup[fav_got_total_line] + ' ' + str(fav_got_total[fav_got_total_line]) + '<br>'
    #print '<br>'
    #for fav_give_total_line in fav_give_total:
       # print id_lookup[fav_give_total_line] + ' ' + str(fav_give_total[fav_give_total_line]) + '<br>'
    #print '<br>'

    if False: '''

    for fav_matrix_line in fav_matrix:
        a = fav_matrix_line.split ('-')
        print str(id_lookup[a[1]]) + ' Liked ' + str(id_lookup[a[0]]) + ' messages number of times ' + str(fav_matrix[fav_matrix_line]) + ' of ' + str(message_count[a[0]]) +' total meessages<br>'
    print '<br>'
    '''

    
    print '<table id="table2">'

    print '<tr> <td></td><td><span style="font-weight:bold">Likes Given</span></td>'
    for user_id3 in id_lookup:
        if id_lookup[user_id3] != 'GroupMe':
            print '<td>' + id_lookup[user_id3] + '</td>'
    print '</tr>'

    print '<tr> <td><span style="font-weight:bold"> Texts tot:' + str(total_count) + '</span></td><td></td>'
    for user_id3 in id_lookup:
        if id_lookup[user_id3] != 'GroupMe':
            if user_id3 in fav_got_total:
                print '<td><span style="font-weight:bold">' + str(user_count_total[user_id3]) + ' %' + str(user_count_avg[user_id3]) + '</span></td>'
            else:
                print '<td></td>'
    print '</tr>'

    print '<tr> <td><span style="font-weight:bold"> Likes in: ' + str(like_total) + '</span></td><td></td>'
    for user_id3 in id_lookup:
        if id_lookup[user_id3] != 'GroupMe':
            if user_id3 in fav_got_total:
                print '<td><span style="font-weight:bold">' + str(fav_got_total[user_id3]) + '</span></td>'
            else:
                print '<td></td>'
    print '</tr>'



    for user_id3 in id_lookup:
        if id_lookup[user_id3] != 'GroupMe':
            print '<tr> <td>' + id_lookup[user_id3] + '</td>'
            if user_id3 in fav_give_total:
                print '<td><span style="font-weight:bold">' + str(fav_give_total[user_id3]) + '</span></td>'
            else:
                print '<td></td>'
            for user_id4 in id_lookup:

                if id_lookup[user_id4] != 'GroupMe':
                    concat = user_id4 + '-' + user_id3
                    if user_id3 == user_id4:
                        isbold = 'font-weight:bold'
                    else:
                        isbold = ''

                    if concat in fav_matrix:
                        #fav_matrix[concat];
                        print '<td><span style="' +isbold + '">' + str(fav_matrix[concat]) + '/' + str(message_count[user_id4]) + '</span></td>'
                    elif user_id4 in message_count:
                        print '<td><span style="' +isbold + '">' + '0' + '/'  + str(message_count[user_id4]) + '</span></td>'
                    else:
                        print '<td><span style="' +isbold + '">' + '0' + '/' + 'UNK' + '</span></td>'
        print '</tr>'
    print '</table>'

    print '<table class="a">'

    for line_print in comment_table:
        print line_print
    print '</table>'

    for avatar_curl in avatar_lines:
        print '<input type=hidden value="' + avatar_lines[avatar_curl] + '">'
    for pic_url in pic_lines:
        print '<input type=hidden value="' + pic_url+ '">'



def main():
    """Usage: simple-transcript.py filename.json

Assumes filename.json is a JSON GroupMe transcript in chronological order.

Times displayed in local timezone.
    """

    if len(sys.argv) < 2:
        print(main.__doc__)
        sys.exit(1)

    transcriptFile = open(sys.argv[1])
    transcript = json.load(transcriptFile)
    transcriptFile.close()

    s = '''<!DOCTYPE html>
    <head>
    <title>GroupMe Chat</title>
    </head>
    <style type="text/css">
    img {
        max-width: 400px;
        height: auto;
        width: auto\9; /* ie8 */
    }

    table, th, td {    border: 1px solid black;    }
    
    td.a {
      border-width:0px; 
      border-color:#000000; 
      
    }
    tr.a {
      border-width:0px; 
      border-color:#000000;  
    }
    table.a {
      border-width:0px; 
      border-color:#000000;        
    }
    </style>

 

    <body>

    <h1>GroupMe Chat Logs</h1>'''
    print (s)


    printTranscript(transcript)
    t = '</body></html>';
    print (t)



if __name__ == '__main__':
    main()
    sys.exit(0)
