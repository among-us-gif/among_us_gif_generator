import hashlib
import json
import os
import random
from PIL import Image, ImageDraw, ImageFont
import numpy as np

from amongusgifgenerator.sprites import ReplaceColors, Skins

all_colors= ['red','blue','green','pink','orange','yellow','grey','white','purple','brown','cyan','line']
all_skins= ['archae','astro','capt','hazmat','mech','military','miner','police','secguard','science','blacksuit','whitesuit','tarmac','wall','winter',None]

def generate_base(image="idle.png", color='blue'):
    body = Image.open(os.path.join("assets", "Sprite", image))
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

def crop_and_save(image, name, type='PNG'):
    if not os.path.exists('scratch'):
        os.makedirs('scratch')
    img = image.copy()
    img = img.crop(img.getbbox())
    img.save(os.path.join('scratch',name), 'PNG')

def generate_all_images():
    for color in all_colors:
        idle = generate_base(image='idle.png', color=color)
        crop_and_save(idle, color+'_idle.png','PNG')
        ejected = generate_base(image='ejected.png', color=color)
        crop_and_save(ejected, color+'_ejected.png','PNG')
        crop_and_save(generate_base(image='Dead0001.png', color=color), color+'_dead.png','PNG')
        crop_and_save(generate_base(image='Dead0040.png', color=color), color+'_dead_floor.png','PNG')
        for skin in all_skins[:-1]:
            idle_body = idle.copy()
            idle_body_origin = (0, 0)
            ejected_body = ejected.copy()
            ejected_body_origin = (0, 0)
            skin_details = Skins(skin=skin)
            idle_skin = Image.open(os.path.join("assets", "Sprite", skin_details.idle))
            eject_skin = Image.open(os.path.join("assets", "Sprite", skin_details.eject))
            idle_body, idle_body_origin = apply_layer(idle_body, idle_skin, skin_details.idle_offset, idle_body_origin)
            crop_and_save(idle_body, color+'_'+skin+'_idle.png', 'PNG')
            ejected_body, ejected_body_origin = apply_layer(ejected_body, eject_skin, skin_details.eject_offset, ejected_body_origin)
            crop_and_save(ejected_body, color+'_'+skin+'_ejected.png', 'PNG')

def make_square(image):
    size = max(image.size)
    new_image = Image.new(image.mode, (size, size), (0, 0, 0, 0))
    new_image.paste(image, (int((size-image.size[0])/2), int((size-image.size[1])/2)), image)
    return new_image

def generate_ejection_message(color=None, skn='rand', person='David', imposter='rand', name=None, path='scratch/gifs/'):
    if imposter == 'rand':
        imposter_options = [False, True, None]
        imposter = imposter_options[random.randrange(0, len(imposter_options))]
    text = person + ' was '
    if imposter == None:
        text += 'ejected.'
    elif imposter == False:
        text += 'not An Imposter.'
    else:
        text += 'An Imposter.'
    if not color:
        color=all_colors[random.randrange(0, len(all_colors))]
    if skn == 'rand':
        skn=all_skins[random.randrange(0, len(all_skins))]
    if not name:
        hasher = hashlib.md5()
        pattern = {'color': color, 'skin': skn, 'hat': None, 'text': text}
        encoded = json.dumps(pattern, sort_keys=True).encode()
        hasher.update(encoded)
        name = hasher.hexdigest()[:8]
    body = generate_base(image='ejected.png', color=color)
    if skn is not None:
        skin_details = Skins(skin=skn)
        skin = Image.open(os.path.join('assets', 'Sprite', skin_details.eject))
        body = apply_layer(body, skin, skin_details.eject_offset, (0, 0))
        body = body[0]
    body = make_square(body)

    font = ImageFont.truetype(os.path.join('assets', 'fonts', 'arial.ttf'), 30)
    text_background = Image.new('RGBA', (1200, 64), (0, 0, 0, 0))
    ImageDraw.Draw(text_background).text((0, 0), text, font=font, fill=(255, 255, 255, 255))
    text_img = text_background.crop(text_background.getbbox())
    center = (int(body.size[0]/2), int(body.size[1]/2))

    eject_gif = []
    background = Image.new('RGBA', (max(text_img.size[0]+100, 600), 300), (0, 0, 0, 255))
    for body_x in range(-100, background.size[0]*3, 12):
        image = background.copy()
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
        eject_gif.append(image)

    if not os.path.exists(path):
        os.makedirs(path)
    eject_gif[0].save(os.path.join(path,name+'.gif'), save_all=True, append_images=eject_gif[1:], duration=40, loop=0)

generate_ejection_message()