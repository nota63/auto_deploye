from django.http import HttpResponse
from django.shortcuts import render, redirect
import pywhatkit as kit
import datetime
from .forms import ContactForm
from datetime import datetime
import wikipediaapi
from django.core.mail import send_mail
from django.conf import settings
import psutil
import platform
import socket
import sys
import speedtest
from PIL import Image, ImageDraw, ImageFont
import os
from handright import Template, handwrite
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import time


def home(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if len(username) > 0 and password == '1234':
            return render(request, 'main.html')
        else:
            return redirect('home')
    return render(request, 'home.html')


def main(request):
    return render(request, 'main.html')


def google(request):
    if request.method == 'POST':
        query = request.POST.get('google')
        kit.search(query)
        return render(request, 'google.html')

    return render(request, 'google.html')


def birthday(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Access cleaned data
            name = form.cleaned_data['name']
            contact = form.cleaned_data['contact']
            birthday = form.cleaned_data['birthday']
            birthday_str = birthday.strftime('%Y-%m-%d')

            # Store data in session
            request.session['name'] = name
            request.session['contact'] = contact
            request.session['birthday'] = birthday_str
            request.session.modified = True  # Mark the session as modified to ensure data is saved

            # Get current date
            current_date = datetime.now().strftime('%Y-%m-%d')
            if birthday_str == current_date:
                message = f"Happy Birthday, {name}! 🎉"
                try:
                    kit.sendwhatmsg_instantly(contact, message)
                    print(f'Sent birthday wish to {name}')
                except Exception as e:
                    print(f'Failed to send message: {e}')

            # Redirect to success page with session data
            session_data = {
                'name': name,
                'contact': contact,
                'birthday': birthday_str,
            }
            return render(request, 'success.html', {'session_data': session_data})

        # If form is not valid, render the form again with errors
        return render(request, 'birthday.html', {'form': form})

    else:
        form = ContactForm()

    # Handle GET requests or rendering the form initially
    session_data = {
        'name': request.session.get('name'),
        'contact': request.session.get('contact'),
        'birthday': request.session.get('birthday'),
    }
    return render(request, 'birthday.html', {'form': form, 'session_data': session_data})


def success(request):
    return render(request, 'success.html')


def youtube(request):
    if request.method == 'POST':
        playlist_url = request.POST.get('yt')
        a = kit.playonyt(playlist_url)
        start = (a)
    return render(request, 'youtube.html')


def playlists(request):
    return render(request, 'playlists.html')


# INITIALIZE WIKIPEDIA- API
wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent="Automation/1.0 (raginimms627@gmail.com)"
)


def info(request):
    if request.method == 'POST':
        try:
            topic = request.POST.get('info')
            page = wiki_wiki.page(topic)
            result = page.summary[:1000000]  # Adjust the length as needed

            data = {
                'result': result
            }

            return render(request, 'info.html', data)
        except ValueError:
            return "valueError"
        except IndexError:
            return "indexError"
        except ConnectionError:
            return "Connection Server Lost"

    return render(request, 'info.html')


def email(request):
    if request.method == 'POST':
        your_email = request.POST.get('your_email')
        password = request.POST.get('password')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        receiver = request.POST.get('receiver')

        # Configure email settings dynamically if needed
        settings.EMAIL_HOST_USER = your_email
        settings.EMAIL_HOST_PASSWORD = password

        try:
            send_mail(
                subject,
                message,
                your_email,
                [receiver],
                fail_silently=False,
            )
            return render(request, 'emailSend.html')
        except Exception as e:
            print(f"Error: {e}")
            return redirect('main')

    return render(request, 'email.html')


def emailSend(request):
    return render(request, 'emailSend.html')


def shutdown(request):
    if request.method == 'POST':
        try:
            sec = int(request.POST.get('sec'))
            kit.shutdown(sec)
            if sec:
                return redirect('home')
            else:
                return redirect('main')
        except ValueError:
            return "Value Should be an int only"
        except ConnectionError:
            return "Please check your network connection"
        except IndexError:
            return "please look at its limits!"
    return render(request, 'shutdown.html')


def system_info(request):
    # Collecting System Information
    system_info = {}

    # CPU Information
    system_info['cpu_count_logical'] = psutil.cpu_count(logical=True)
    system_info['cpu_count_physical'] = psutil.cpu_count(logical=False)
    system_info['cpu_usage'] = psutil.cpu_percent(interval=1)
    system_info['cpu_times'] = psutil.cpu_times()

    # Memory Information
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    system_info['total_memory'] = memory.total / (1024 ** 3)
    system_info['available_memory'] = memory.available / (1024 ** 3)
    system_info['used_memory'] = memory.used / (1024 ** 3)
    system_info['memory_usage'] = memory.percent
    system_info['total_swap'] = swap.total / (1024 ** 3)
    system_info['used_swap'] = swap.used / (1024 ** 3)
    system_info['free_swap'] = swap.free / (1024 ** 3)
    system_info['swap_usage'] = swap.percent

    # Disk Information
    partitions = psutil.disk_partitions()
    disk_info = []
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        disk_info.append({
            'device': partition.device,
            'mountpoint': partition.mountpoint,
            'fstype': partition.fstype,
            'total': usage.total / (1024 ** 3),
            'used': usage.used / (1024 ** 3),
            'free': usage.free / (1024 ** 3),
            'percent': usage.percent,
        })
    io = psutil.disk_io_counters()
    system_info['disk_info'] = disk_info
    system_info['read_count'] = io.read_count
    system_info['write_count'] = io.write_count
    system_info['read_bytes'] = io.read_bytes
    system_info['write_bytes'] = io.write_bytes

    # Network Information
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    system_info['hostname'] = hostname
    system_info['ip_address'] = ip_address
    interfaces = psutil.net_if_addrs()
    network_info = []
    for interface, addresses in interfaces.items():
        interface_info = {'interface': interface, 'addresses': []}
        for address in addresses:
            interface_info['addresses'].append({
                'address': address.address,
                'netmask': address.netmask,
                'broadcast': address.broadcast,
            })
        network_info.append(interface_info)
    net_io = psutil.net_io_counters()
    system_info['network_info'] = network_info
    system_info['bytes_sent'] = net_io.bytes_sent
    system_info['bytes_received'] = net_io.bytes_recv

    # System Information
    system_info['platform'] = platform.system()
    system_info['platform_version'] = platform.version()
    system_info['platform_release'] = platform.release()
    system_info['architecture'] = platform.machine()
    system_info['processor'] = platform.processor()

    # Python Version
    system_info['python_version'] = sys.version

    # Process Information
    process_info = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        process_info.append({
            'pid': proc.info['pid'],
            'name': proc.info['name'],
            'username': proc.info['username'],
        })

    context = {
        'system_info': system_info,
        'process_info': process_info,
    }

    return render(request, 'system_info.html', context)


def speed(request):
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        ping = st.results.ping
        server = st.results.server['name']
        isp = st.results.client['isp']

        speed_data = {
            'download_speed': download_speed,
            'upload_speed': upload_speed,
            'ping': ping,
            'server': server,
            'isp': isp,
        }

        return render(request, 'speed.html', {'speed_data': speed_data})
    except Exception as e:
        return render(request, 'speed.html', {'error': str(e)})


def image(request):
    if request.method == 'POST':
        image_path = request.POST.get('image_path')
        if not image_path:
            return render(request, 'image.html', {'error': 'Image path is required.'})

        # Convert image to ASCII art
        ascii_art = kit.image_to_ascii_art(image_path)

        # Set up font and image parameters
        try:
            font = ImageFont.truetype("arial.ttf", 15)
        except IOError:
            font = ImageFont.load_default()

        lines = ascii_art.split('\n')
        dummy_image = Image.new('RGB', (1, 1))
        draw = ImageDraw.Draw(dummy_image)

        max_width = max([draw.textbbox((0, 0), line, font=font)[2] for line in lines])
        line_height = draw.textbbox((0, 0), 'A', font=font)[3]
        image_height = line_height * len(lines)

        # Create an image canvas to draw text
        image = Image.new('RGB', (max_width, image_height), color='white')
        draw = ImageDraw.Draw(image)

        # Draw the ASCII art on the canvas
        for i, line in enumerate(lines):
            draw.text((0, i * line_height), line, fill='black', font=font)

        # Save the image as PNG
        output_path = os.path.join('media', 'ascii_art.png')
        image.save(output_path)

        return render(request, 'image.html', {'image_path': output_path})

    return render(request, 'image.html')


def text_to_handwriting(request):
    if request.method == "POST":
        text = request.POST.get("text", "")
        if text:
            # Define the template for handwriting
            template = Template(
                background=Image.new("RGB", (800, 1000), (255, 255, 255)),
                font=ImageFont.truetype("arial.ttf", 50),  # Change to your font path if needed
                line_spacing=100,
                fill=(0, 0, 0),
            )

            # Create handwritten pages
            images = list(handwrite(text, template))  # Convert map object to a list

            if not images:
                return HttpResponse("Handwriting generation failed.", content_type="text/plain")

            # Save the first page to an in-memory file
            img_io = BytesIO()
            images[0].save(img_io, format="PNG")
            img_io.seek(0)

            # Save the image to the media folder
            output_path = os.path.join(settings.MEDIA_ROOT, 'handwritten.png')
            images[0].save(output_path)

            # Pass the image URL to the template
            image_url = os.path.join(settings.MEDIA_URL, 'handwritten.png')
            return render(request, "text_to_handwriting.html", {'image_url': image_url})
        else:
            return HttpResponse("No text provided.", content_type="text/plain")

    return render(request, "text_to_handwriting.html")


def whatsapp_image(request):
    if request.method == 'POST':
        contact = request.POST.get('contact')
        image_path = request.POST.get('image_path')
        caption = request.POST.get('caption')

        try:
            # Sending image using pywhatkit
            kit.sendwhats_image(contact, image_path, caption)

            # Adding a delay to ensure the image is sent
            time.sleep(1)  # Adjust the delay as necessary

            return render(request, 'whatsapp_image.html', {'message': 'Image sent successfully!'})
        except Exception as e:
            return render(request, 'whatsapp_image.html', {'error': str(e)})

    return render(request, 'whatsapp_image.html')


def multi_whatsapp(request):
    if request.method == 'POST':
        numbers = request.POST.get('numbers')
        message = request.POST.get('message')

        numbers_list = numbers.split(',')

        try:

            for number in numbers_list:
                number = number.strip()
                kit.sendwhatmsg_instantly(number, message)
                time.sleep(2)

            return render(request, 'multi_whatsapp.html', {'message': 'Messages sent successfully!'})
        except Exception as e:
            return render(request, 'multi_whatsapp.html', {'error': str(e)})

    return render(request, 'multi_whatsapp.html')


def myself(request):
    return render(request, 'myself.html')
