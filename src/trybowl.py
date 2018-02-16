'''Main Function Runner'''

from albertbowl import SoupBowl

# test
bowl = SoupBowl()
bowl.serve('https://bitcointalk.org/index.php?topic=2889704.0;all')

boxes = bowl.scoop('#quickModForm').scoop('tbody').scoop('tr').taste()

forum_data = []
print(boxes[2])
for box in boxes:
    threadOrigin = bowl.serve(html=box)
    data = {}

    try:
        data['author'] = {}
        data['author']['name'] = threadOrigin.scoop('.poster_info').scoop('tag.name(b)').scoop('a').taste('fin')[0] # name
        data['author']['title'] = threadOrigin.scoop('.poster_info').scoop('div').taste('fin')[0][0].strip() # title

        data['content'] = {}
        data['content']['title'] = threadOrigin.scoop('.td_headerandpost').scoop('.subject').scoop('a').taste('fin')[0] # header
        data['content']['date'] = threadOrigin.scoop('.td_headerandpost').scoop('.smalltext').taste('fin')[0] # date
        data['content']['message'] = threadOrigin.scoop('.td_headerandpost').scoop('.post').taste('fin')[0][-1] # msg

        data['content']['quote'] = {}
        data['content']['quote']['title'] = threadOrigin.scoop('.td_headerandpost').scoop('.post').scoop('.quoteheader').taste('fin')[0]
        data['content']['quote']['message'] = threadOrigin.scoop('.td_headerandpost').scoop('.post').scoop('.quote').taste('fin')

        forum_data.append(data)
    except Exception as e:
        pass

print(forum_data)

threadMessages = boxes[3:]
