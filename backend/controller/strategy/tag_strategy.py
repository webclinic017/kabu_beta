from  backend.model.tag import TAG

class TagStrategy:

    def getResult(self,words):
        result =[]
        taglist = TAG.objects.all()
        for tag in taglist:

            if words.find(tag.tag_name)>0:
                result.append(tag.tag_name)

        return result;