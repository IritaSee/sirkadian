from imagekitio import ImageKit

def cdn_url(type,filename):
    cdn_url = 'https://ik.imagekit.io/sirkadian'
    if type == 'food':  
        return cdn_url + '/food_image/' + filename
    else: 
        return cdn_url

cdn = ImageKit(
    private_key='private_MUQa7MbNTuXZP3Fn4+lkLM5Ar2Q=',
    public_key='public_pVPb+Sld2L1h5mwlUTJdirpMjyc=',
    url_endpoint=cdn_url
)
