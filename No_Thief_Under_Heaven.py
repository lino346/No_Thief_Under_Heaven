# -*- coding:utf-8 -*-
"""
author: 11238
date: 2021year 10month 10day
"""
import pygame

from midi_and_metronome import metronome
from midi_and_metronome import play_note

from score_function import generate_score, percentage

from midi_note import midi_note

from recording import recordingTool

import time as ti

import sys

from pygame.sprite import Group

from screen import Settings

import game_function as gf

from Thief import Thief

from Police import Police

import pyaudio
from lino_settings import lino_settings
#import game_functions as gf

def run_game():
    
    pygame.init()
    ai_settings = Settings()
    # inputFile = input("Please input your file name:")
    # # PATH_TO_MIDI = '/home/lino/Desktop/group 6/test_CSD/midi/en0{}a.mid'.format(inputFile)
    # PATH_TO_MIDI = '/home/lino/Desktop/group 6/test_POP909/{}.mid'.format(inputFile)
    
    # ai_settings.midi = PATH_TO_MIDI
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    ai_settings.rect = screen.get_rect()
    pygame.display.set_caption('No Thief Under Heaven')
    ai_settings.background = pygame.transform.scale(ai_settings.background,(ai_settings.screen_width+1,ai_settings.screen_height)).convert()
    score_ratio=0.5
    ai_settings.score = pygame.transform.scale(ai_settings.score,(int(ai_settings.score.get_width()*ai_settings.screen_height * score_ratio/ai_settings.score.get_height()), int(ai_settings.screen_height * score_ratio))).convert_alpha()
    screen.blit(ai_settings.background, (0, 0))
    ti.sleep(1)
    play_note(ai_settings.firstPitch,1, octave = ai_settings.firstPitch//12)
    pygame.display.flip()
    ti.sleep(1)

    thief = Thief(ai_settings, screen)
    police=Police(ai_settings, screen, 1)
    step=0
    step_score=0.1034*ai_settings.score_width
    image_Win = pygame.image.load('you_win2.png')
    image_Win=pygame.transform.scale(image_Win,(int(image_Win.get_width()*73/670), int(image_Win.get_height()*73/670))).convert_alpha()
    win=False
    image_Lose=pygame.image.load('game_over.png')
    lose=False
    time=0
    tempo_para=1000
    timelimited=ai_settings.score.get_width()*tempo_para/ai_settings.tempo-500
    block_time=0
    step_time=0
    only_m=0

    p = pyaudio.PyAudio()
    lino = lino_settings()
    # open stream
    stream = p.open(format=lino.pyaudio_format,
                    channels=lino.n_channels,
                    rate=lino.samplerate,
                    input=True,
                    frames_per_buffer=lino.buffer_size)

    # setup pitch
    lino.pitch_o.set_unit("midi")
    lino.pitch_o.set_tolerance(lino.tolerance)
    gt_arr, tempo, total_step = lino.midi_arr('080.mid')
    index = 0
    step_cur = 0
    pitch_list = []
    police_speed = 0
    thief_position = thief.rect.centerx

    while True:
        if not only_m==0:
            gf.update_screen(ai_settings, screen, thief, police, step, step_score, win, image_Win, lose, image_Lose,police_speed)
            
        else:
            metronome(ai_settings.bpm, 4)
            only_m=1
            time_lino = ti.time()

        
        time_start=ti.time()
        time+=1
        # if time>=timelimited:
        #     lose=True
        # if thief.rect.centerx-police.rect.centerx<=10 and not lose:
        #     win=True

        gf.check_events(ai_settings, screen, thief, police)
        
        
        audiobuffer = stream.read(lino.buffer_size)
        pitch = lino.get_pitch(audiobuffer)
        t_cur = ti.time() - time_lino
        
        gt_cur = lino.get_gt(t_cur, gt_arr[index,:])
        if lino.score_strategy(gt_cur, pitch, t_cur, gt_arr[0,0]) == True :
            score = 'null'
        else:
            score = generate_score(pitch, gt_cur)
            pitch_list.append(pitch)
        
        
        # print("pitch_est = {}, pitch_ref = {}, score = {}".format(pitch, gt_cur, score))      

        # police_speed=0
        
        if time%20==0:
            thief.update()
            police.update()
        
        step += ai_settings.thief_speed_factor
        time_end = ti.time()
        step_score += 2.65*step_time/ai_settings.end_time*(1-0.1144)*ai_settings.score_width
        
        step_time=time_end-time_start

        if t_cur > gt_arr[index, 1] and index != gt_arr.shape[0]-1:
            step_cur = lino.policeman_step(pitch_list, gt_arr[index, 3], step_cur)
            
            police.rect.centerx = lino.policeman_move(step_cur, total_step, thief_position)
            index += 1
            pitch_list=[]
            print("----------------------------------------To win, you need:", total_step - step_cur, " more steps!------------------------------------------")
            if total_step == step_cur:
                win = True
                print('----------------------------------------You Win!!!------------------------------------------')
                print('Total steps to win:{}, you spend:{} '.format(total_step, index))
            score_tmp = []
        
        if index == gt_arr.shape[0]-1 and t_cur > gt_arr[index, 1]:
            percent = percentage(score_tmp)
            score_tmp = []
            lose = True

run_game()