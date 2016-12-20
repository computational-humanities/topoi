def ImageRegistration(imagelist, reference):
    """
    Estimates the (affine) transformation matrix between two images. This procedure depends on a server with Mathematica 
    installation. Please note that image transformation might take a while depending on image size. 

    :param reference: path/name to reference image (e.g. ortho foto of an object or overview image) 
    :type reference: string
    :param imagelist: one or more images for transformation procedure
    :type imagelist: list
    
    :returns: only data export
    
    :example:
        >>> 
        
    """
    for x in range(0, len(imagelist)):
        print('execute script: math -script run_registration.m '+reference[0]+' '+imagelist[x])
        script = 'math -script run_registration.m  '+reference[0]+' '+imagelist[x]
        p = sub.Popen(['ssh', 'mathematica@141.20.159.97',script],stdout=sub.PIPE,stderr=sub.PIPE) 
    return;
