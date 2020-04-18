#!/usr/bin/python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from random import randrange,random
import smtplib
from playsound import playsound
import os
import sys
import optparse
from multiprocessing import Process

CWD = os.path.dirname(os.path.abspath(__file__))




AMZ_URL = "https://www.amazon.com/"




def init_conf():
    
    parser = optparse.OptionParser('%prog [options]')
    parser.add_option("-u", "--amzuser", default='',
                      action="store", type="string", dest="amz_user",
                      help = "amazon user, required ")

    parser.add_option("-p", "--amzpass", default='',
                      action="store", type="string", dest="amz_pass",
                       help = "amazon password, required")

    parser.add_option("-c", "--cartype", default='wf',
                      action="store", type="string", dest="cart_type",
                      help = "cart type: 'wf' or 'af' default: wf")
    
    parser.add_option("-m", "--smtpserv", default='smtp.gmail.com',
                      action="store", type="string", dest="smtp_serv",
                      help = "smtp server for sending SMS alert")
    parser.add_option("-s", "--smtpuser", default='',
                      action="store", type="string", dest="smtp_user",
                      help = "smtp mail server account")
    parser.add_option("-a", "--smtppass", default='',
                      action="store", type="string", dest="smtp_pass",
                      help = "smtp mail server password")

    parser.add_option("-n", "--sms_number", default='',
                      action="store", type="string", dest="sms_num",
                      help = "cellphone number for SMS alert")
    parser.add_option("-i", "--insane", 
                      action="store_true", dest="insane",
                      help = "insane mode: desperately grab slot and auto checkout")

    (options, args) = parser.parse_args()

    if options.amz_user == '' or options.amz_pass == '':
        sys.exit("amazon user and pass can not be empty")

    return options
    
    

def do_check_wf_cart(conf):
    try:
        
        play_process = Process(target=playsound, args=('success.mp3',)) # alerting process
        chrome_options = Options()  
        #chrome_options.add_argument("--headless")  
        #chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(AMZ_URL)

        driver.implicitly_wait(20)
        sleep(random()*2)
        driver.find_element_by_link_text('Your Orders').click()
        e = driver.find_element_by_id('ap_email')
        e.click()
        e.send_keys(conf.amz_user)
        sleep(random()*3)
        driver.find_element_by_id('continue').click()
        
        e = driver.find_element_by_id('ap_password')
        sleep(random()*3)
        e.click()
        e.send_keys(conf.amz_pass)
        sleep(random()*2)
        driver.find_element_by_id('auth-signin-button').click()

        driver.find_element_by_id('nav-cart-count')
        sleep(random()*3)
        driver.find_element_by_id('nav-cart').click()

        driver.find_element_by_id('sc-subtotal-amount-buybox')
        e = driver.find_element_by_name(
            'proceedToALMCheckout-VUZHIFdob2xlIEZvb2Rz')
        sleep(random()*3)
        e.submit()
        sleep(random()*3)
        driver.find_element_by_name('proceedToCheckout').click()
        sleep(random()*3)
        driver.find_element_by_id('subsContinueButton').click()


        
        slot_found = False
        ntrial = 0
        
       

        while slot_found == False:
            e = driver.find_elements_by_class_name(
            'ufss-date-select-toggle-text-availability')
            for i in e:
                print(i.text)
                if (i.text != 'Not available'):
                    slot_found = True
                    play_process.start()  # async play music
                    if conf.smtp_user != '':
                        send_mail(conf.smtp_serv,
                                  conf.smtp_user, conf.smtp_pass,
                                  conf.smtp_user, conf.sms_num+'@txt.att.net',
                                  'pangbot alert!')
                    
                    if conf.insane == False:
                        input('time slot found! Please checkout in the browser then push any key to continue.')
                    else:
                        slots = driver.find_elements_by_class_name('ufss-slot-toggle-native-button')
                        for slot in slots:
                            print("slot text: %s" % (slot.text))
                            if slot.text == 'FREE':
                                slot.click()
                                driver.find_elements_by_class_name('a-button-input').submit()
                                sleep(random())
                                driver.find_elements_by_class_name('a-button-input').submit()
                                driver.find_element_by_name('placeYourOrder1').submit()
                                input('Order placed. Play check the order status and push any key to continue')

                                break
                            


                    break
            
            sleep_time = randrange(20,40)
            print("sleeping %d.." % (sleep_time))
            sleep(sleep_time)
            driver.refresh()
            ntrial += 1
            print("retry %d times.\n" % ntrial)
            
                              
    except:
        print('error executing actions.')
    finally:
        sleep(20)
        play_process.terminate()
        play_process.join(1)
        driver.quit()
            
def do_check_af_cart(conf):
    try:
        
        chrome_options = Options()  
        #chrome_options.add_argument("--headless")  
        #chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        #chrome_options.add_argument("user-data-dir="+CWD+"\\foo")
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(AMZ_URL)

        driver.implicitly_wait(20)
        sleep(random()*3)
        driver.find_element_by_link_text('Your Orders').click()
        e = driver.find_element_by_id('ap_email')
        e.click()
        e.send_keys(conf.amz_user)
        sleep(random()*3)

        driver.find_element_by_id('continue').click()
        e = driver.find_element_by_id('ap_password')
        e.click()
        e.send_keys(conf.amz_pass)
        sleep(random()*3)
        driver.find_element_by_id('auth-signin-button').click()

        driver.find_element_by_id('nav-cart-count')
        driver.find_element_by_id('nav-cart').click()

        driver.find_element_by_id('sc-subtotal-amount-buybox')
        e = driver.find_element_by_name(
            'proceedToALMCheckout-QW1hem9uIEZyZXNo')
        e.submit()
        driver.find_element_by_name('proceedToCheckout').click()

        slot_found = False
        while slot_found == False:
            e = driver.find_elements_by_class_name(
                'ufss-date-select-toggle-text-availability')
            
            for i in e:
                print(i.text)
                if (i.text != 'Not available'):
                    slot_found = True
                    playsound(CWD+'\\success.mp3', block=False)
                    if conf.smtp_user != '':
                        send_mail(conf.smtp_serv,
                                  conf.smtp_user, conf.smtp_pass,
                                  conf.smtp_user, conf.sms_num+'@txt.att.net',
                                  'pangbot alert!')
                    
                    input('time slot found! push any key to continue.')
                    break
                
            sleep(randrange(10,30))
            driver.refresh()
                              
    except:
        print('error executing actions.')
    finally:
        sleep(3)
        driver.quit()        

def send_mail(smtp_server, user, passwd, sender, recvr, msg):
    try:
        server = smtplib.SMTP_SSL(smtp_server, 465)
        server.ehlo()
        server.login(user, passwd)
        server.sendmail(sender, recvr, msg)
    except:
        print('Something went wrong...')
    finally:
        server.quit()


def main():

    conf = init_conf()
    print("PangBot configuration summary:")
    print(conf)
    while True:
        if conf.cart_type == 'wf':
            do_check_wf_cart(conf)
        elif conf.cart_type == 'af':
            do_check_af_cart(conf)
        else:
            print("cart type not supported.\n")
        sleep(20)


if __name__ == "__main__":
    main()
