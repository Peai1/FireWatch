from django.shortcuts import render, redirect
from folium.features import ClickForMarker
from .models import Search, Comment
from .forms import SearchForm, Latitud_Longitud, ComentariosForm
import folium
import geocoder
from geopy.geocoders import Nominatim # para obtener la el nombre de la ubicación según la latitud y longitud
from ipware import get_client_ip # obtener ip
import sqlite3
import time
import datetime


# Create your views here.

def inicio(request):
    return render(request, 'inicio.html')

def incendios(request):
    return render(request, 'incendios.html')




def crear_mapa(request):
    if len(Search.objects.all())>=1:
        address = Search.objects.all()[(len(Search.objects.all())-1)]
        location = geocoder.osm(address)
        lat = location.lat
        lng = location.lng
        m = folium.Map(location=[lat,lng], zoom_start=7)
    else:
        m = folium.Map(location=[-30,-65], zoom_start=7)

    basededatos = Search.objects.all()
    for direccion in basededatos:
        ubic = geocoder.osm(direccion)
        lati = ubic.lat
        lngt = ubic.lng
        folium.Marker(location=[lati, lngt],icon=folium.Icon(icon='glyphicon-fire', color='red'), tooltip='Clic para conocer la ubicación del incendio',
                  popup=direccion).add_to(m) 
    
    m = m._repr_html_()   
    
    return m

def mostrar_mapa(request):
    all_comments = Comment.objects.all()   
    context = {
        'm': crear_mapa(request),
        'all':all_comments,
    }
    return render(request, 'index.html', context)

def comentarios(request):
    all_comments = Comment.objects.all()

    if request.method == 'POST':
        form = ComentariosForm(request.POST)
        nombre = request.POST['nombre']
        body = request.POST['body']
        ins = Comment(commenter_name=nombre,comment_body=body)
        if form.is_valid():
            ins.save()
            return redirect('mostrar_mapa')
    else:
        form = ComentariosForm()

    context = {
        'all':all_comments,
        'form':form,
    }

    return render(request,'comentarios.html',context)

def ingresar_direccion(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mostrar_mapa')
    else:
        form = SearchForm()
    #if lat == None or lng == None:
    #    address.delete()
    #    return HttpResponse('La dirección ingresada es invalida')  
    context = {
        'm': crear_mapa(request),
        'form': form,
    }
    return render(request, 'buscar.html', context)


def ubicacion_usuario(request): 
    
    ip = direccion_ip(request) # "45.232.95.203"  "68.182.34.151" 
    g = geocoder.ip("68.182.34.151") 
    geolocator = Nominatim(user_agent='geoapiExercises')
    latitude = str(g.lat)
    longitude = str(g.lng)
    location = geolocator.reverse(latitude+','+longitude)
    address = location.raw['address']
    ciudad = address.get('city', '')
    estado = address.get('state', '')
    pais = address.get('country', '')
    popup = ciudad+','+estado+','+pais

    ingresar_basededatos(popup)
    return redirect('mostrar_mapa')    

def puntero(request):
    if request.method == 'POST':
        form = Latitud_Longitud(request.POST)
        if form.is_valid():
            ubic = form.cleaned_data['post']
            geolocator = Nominatim(user_agent='geoapiExercises')
            location = geolocator.reverse(ubic)
            address = location.raw['address']
            ciudad = address.get('city', '')
            estado = address.get('state', '')
            pais = address.get('country', '')
            popup = ciudad+','+estado+','+pais
            ingresar_basededatos(popup)
            return redirect('mostrar_mapa')
    else:
        form = Latitud_Longitud()
    
    m = folium.Map(location=[-30,-65], zoom_start=3)  
    
    ClickForMarker().add_to(m)

    basededatos = Search.objects.all()
    for direccion in basededatos:
        ubic = geocoder.osm(direccion)
        lati = ubic.lat
        lngt = ubic.lng
        folium.Marker(location=[lati, lngt],icon=folium.Icon(icon='glyphicon-fire', color='red'), tooltip='Clic para conocer la ubicación del incendio',
                  popup=direccion).add_to(m)  
           
    m = m._repr_html_()
    context = {
            'm': m,
            'form': form,
    }
    return render(request, 'formulario.html', context)

def direccion_ip(request):   
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def ingresar_basededatos(address):
    
    unix = int(time.time())
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    sqlite_insert_with_param = """INSERT INTO map_search
                          (address, date) 
                           VALUES 
                          (?,?);"""
    data_tuple = (address,date)
    c.execute(sqlite_insert_with_param, data_tuple)
    conn.commit()
    c.close()
    
def basededatos_comentarios(nombre,body):
    unix = int(time.time())
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    sqlite_insert_with_param = """INSERT INTO map_search
                          (commenter_name, comment_body, date_added) 
                           VALUES 
                          (?,?);"""
    data_tuple = (nombre,body,date)
    c.execute(sqlite_insert_with_param, data_tuple)
    conn.commit()
    c.close()
