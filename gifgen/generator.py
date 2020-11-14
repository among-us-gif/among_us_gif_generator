import hashlib
import json
import os
import random
from PIL import Image, ImageDraw, ImageFont
import numpy as np

from gifgen.sprites import ReplaceColors, Skins

ASSET_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')

all_colors= ['red','blue','green','pink','orange','yellow','grey','white','purple','brown','cyan','lime']
all_skins= ['archae','astro','capt','hazmat','mech','military','miner','police','secguard','science','blacksuit','whitesuit','tarmac','wall','winter',None]

def generate_base(image="idle.png", color='blue'):
    """
    Generates a base image for an Among Us Asset that needs color replacement.
    The default image is the standing crewmate (idle) and the default color is blue.

    :param image: The image to load up
    :type image: str
    :param color: The color to make the base image, must be one of red, blue, green, 
                  pink, orange, yellow, grey, white, purple, brown, cyan, or lime
    :type color: str
    """
    body = Image.open(os.path.join(ASSET_PATH, image))
    return color_replace(image=body, color=ReplaceColors(color=color))

def color_replace(image=None, color=None):
    if not color:
        color = ReplaceColors()
    im = image.convert('RGBA')
    pixels = np.array(im)
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            pixel = pixels[j][i]
            if pixel[3] > 0 and not (pixel[0] == pixel[1] and pixel[1] == pixel[2] and pixel[0] == pixel[2]):
                if sum([1 if (value >= 45 and value <= 65) else 0 for value in pixel[:3]]) < 3:
                    new_pixel_green = [int(value * pixel[1] / 255) for value in color.green]
                    if pixel[1] == 0 or (sum(pixel) >= 508 and sum(pixel) <= 520):
                        new_pixel_red = [int(value * pixel[0] / 255) for value in color.red]
                        new_pixel_blue = [int(value * pixel[2] / 255) for value in color.blue]
                    elif pixel[0] == pixel[2] and sum(pixel) > 512:
                        new_pixel_red = new_pixel_blue = [int(((pixel[0]/255) * (255-value))/2) for value in new_pixel_green]
                    else:
                        new_pixel_red = [int(pixel[0]/255)]*3
                        new_pixel_blue = [int(pixel[2]/255)]*3
                    new_pixel = [min(new_pixel_red[i] + new_pixel_green[i] + new_pixel_blue[i], 255) for i in range(3)]
                    new_pixel.append(pixel[3])
                    pixels[j][i] = new_pixel
    return Image.fromarray(pixels)

def apply_layer(base_image, layer_image, layer_origin, base_origin=(0, 0)):
    base_width, base_height = base_image.size
    layer_width, layer_height = layer_image.size
    left = layer_origin[0] + base_origin[0]
    left = abs(left) if left < 0 else 0
    top = layer_origin[1] + base_origin[1]
    top = abs(top) if top < 0 else 0
    right = layer_origin[0] + layer_width - base_width
    bottom = layer_origin[1] + layer_height - base_height
    new_image = Image.new(base_image.mode, (left+right+base_width, top+bottom+base_height), (0, 0, 0, 0))
    base_origin = (left, top)
    new_layer_origin = (base_origin[0]+layer_origin[0], base_origin[1]+layer_origin[1])
    new_image.paste(base_image, base_origin, base_image)
    new_image.paste(layer_image, new_layer_origin, layer_image)
    return new_image, base_origin

def crop_and_save(image, name, path='scratch', type='PNG'):
    if not os.path.exists(path):
        os.makedirs(path)
    img = image.copy()
    img = img.crop(img.getbbox())
    img.save(os.path.join(path,name), 'PNG')

def generate_crewmate(color='blue', skn=None, ejected=True):
    skin = Skins(skin=skn) if skn else None
    if ejected:
        body = generate_base(image='ejected.png', color=color)
        body_origin = (0, 0)
        if skin:
            skin_im = Image.open(os.path.join(ASSET_PATH, skin.eject))
            body, body_origin = apply_layer(body, skin_im, skin.eject_offset)
    else:
        body = generate_base(image='idle.png', color=color)
        body_origin = (0, 0)
        if skin:
            skin_im = Image.open(os.path.join(ASSET_PATH, skin.idle))
            body, body_origin = apply_layer(body, skin_im, skin.idle_offset)
    return body, body_origin

def generate_all_images(path='scratch'):
    for color in all_colors:
        crop_and_save(generate_base(image='Dead0001.png', color=color), color+'_dead.png', path=path, type='PNG')
        crop_and_save(generate_base(image='Dead0040.png', color=color), color+'_dead_floor.png', path=path, type='PNG')
        crop_and_save(generate_base(image='ghostbob0001.png', color=color), color+'_ghostbob0001.png', path=path, type='PNG')
        for skin in all_skins:
            ejected_body, body_origin = generate_crewmate(color=color, skn=skin, ejected=True)
            crop_and_save(ejected_body, color+'_'+skin+'_ejected.png', path=path, type='PNG')
            idle_body, body_origin = generate_crewmate(color=color, skn=skin, ejected=True)
            crop_and_save(idle_body, color+'_'+skin+'_idle.png', path=path, type='PNG')

def make_square(image):
    size = max(image.size)
    new_image = Image.new(image.mode, (size, size), (0, 0, 0, 0))
    new_image.paste(image, (int((size-image.size[0])/2), int((size-image.size[1])/2)), image)
    return new_image

def generate_stars(width=2000):
    base = Image.new('RGBA', (width, 588), (0, 0, 0, 0))
    stars = Image.open(os.path.join(ASSET_PATH, 'Stars.png'))
    stars = stars.rotate(90)
    stars2 = stars.copy().rotate(180)
    for x in range(-800, width, 320):
        base.paste(stars2, (x, int(x/60)-200), stars2)
        base.paste(stars, (x, 100+int(x/120)), stars)
        base.paste(stars2, (x, 300-int(x/60)), stars2)
        base.paste(stars, (x, 500+int(x/120)), stars)
        base.paste(stars, (x+160+int(x/80), int(x/100)-100), stars)
        base.paste(stars2, (x+160-int(x/80), 100+int(x/120)), stars2)
        base.paste(stars, (x+160+int(x/80), 300-int(x/100)), stars)
        base.paste(stars2, (x+160-int(x/80), 500-int(x/100)), stars2)
    return base

def generate_ejection_message(color=None, skn='rand', person='I', impostor='rand', name=None, path='scratch/gifs/'):
    if impostor == 'rand':
        impostor_options = [False, True, None]
        impostor = impostor_options[random.randrange(0, len(impostor_options))]
    text = person + ' was '
    if impostor == None:
        text += 'ejected.'
    elif impostor == False:
        text += 'not An Impostor.'
    else:
        text += 'An Impostor.'
    return generate_ejection_gif(color=color, skn=skn, hat=None, text=text, add_stars=1, path=path, name=name, watermark=True)

def generate_ejection_custom_message(color=None, skn='rand', text="I have been ejected.", path='scratch/gifs/'):
    return generate_ejection_gif(color=color, skn=skn, hat=None, text=text, add_stars=1, path=path, name=None, watermark=True)


def generate_ejection_gif(color='blue', skn='rand', hat=None, text="I have been ejected.", add_stars=True, path='scratch/gifs/', name=None, watermark=True):
    if not color:
        color=all_colors[random.randrange(0, len(all_colors))]
    if skn == 'rand':
        skn=all_skins[random.randrange(0, len(all_skins))]
    if not name:
        hasher = hashlib.md5()
        pattern = {'color': color, 'skin': skn, 'hat': hat, 'text': text, 'stars': add_stars, 'watermark': watermark}
        encoded = json.dumps(pattern, sort_keys=True).encode()
        hasher.update(encoded)
        name = hasher.hexdigest()[:16]
    if os.path.exists(os.path.join(path, name+'.gif')):
        return name+'.gif'
    body, body_origin = generate_crewmate(color=color, skn=skn, ejected=True)
    body = make_square(body)

    font = ImageFont.truetype(os.path.join(ASSET_PATH, 'arial.ttf'), 30)
    text_background = Image.new('RGBA', (4000, 64), (0, 0, 0, 0))
    ImageDraw.Draw(text_background).text((0, 0), text, font=font, fill=(255, 255, 255, 255))
    text_img = text_background.crop(text_background.getbbox())
    center = (int(body.size[0]/2), int(body.size[1]/2))

    watermark_font = ImageFont.truetype(os.path.join(ASSET_PATH, 'impact.ttf'), 24)
    watermark_background = Image.new('RGBA', (200, 48), (0, 0, 0, 0))
    ImageDraw.Draw(watermark_background).text((0, 0), 'Amongusgif.com', font=watermark_font, fill=(40, 40, 40, 255))
    watermark_img = watermark_background.crop(watermark_background.getbbox())

    eject_gif = []
    background = Image.new('RGBA', (max(text_img.size[0]+100, 600), 300), (0, 0, 0, 255))
    if add_stars:
        stars = generate_stars(background.size[0]*3)
        stars1 = stars.resize((int(stars.size[0]*3.5), int(stars.size[1]*3.5)), Image.ANTIALIAS)
        stars2 = stars1.copy()
        stars3 = stars1.copy()
    for body_x in range(-120, background.size[0]*3, 12):
        image = background.copy()
        if add_stars:
            image.paste(stars1, (int(-background.size[0]+body_x/24)-100, -200), stars1)
            image.paste(stars2, (int(-background.size[0]+body_x/12)-200, -800), stars2)
            image.paste(stars3, (int(-background.size[0]+body_x/6)-100, -425), stars3)
        txt = text_img.copy()
        if body_x > int(background.size[0]/2) and body_x <= int(3*background.size[0]/2):
            mid_x = int(background.size[0]/2)
            text_y = int(background.size[1]/2-txt.size[1]/2)
            text_x = int(mid_x-((body_x-mid_x)/background.size[0])*txt.size[0]/2)
            final_txt = txt.crop((0, 0, int(mid_x-text_x)*2, txt.size[1]))
            image.paste(final_txt, (text_x, text_y), final_txt)
            pass
        elif body_x > int(background.size[0]*1.5) and body_x <= int(background.size[0]*2.5):
            image.paste(txt, (int(background.size[0]/2-txt.size[0]/2), int(background.size[1]/2-txt.size[1]/2)), txt)
        rotated_body = body.copy().rotate(int(2*body_x/3))
        image.paste(rotated_body, (int(body_x-center[0]), int((background.size[1]/2)-center[1])), rotated_body)
        if watermark:
            image.paste(watermark_img, (background.size[0]-watermark_img.size[0]-5, background.size[1]-watermark_img.size[1]-5), watermark_img)
        eject_gif.append(image)

    if not os.path.exists(path):
        os.makedirs(path)
    eject_gif[0].save(os.path.join(path,name+'.gif'), save_all=True, append_images=eject_gif[1:], duration=40, loop=0)
    return name+'.gif'
