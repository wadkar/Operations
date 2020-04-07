from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView

from django.shortcuts import render

# Create your views here.
from gocorona_api.users.models import CoronaApp
from gocorona_api.users.api.serializers import CoronaAppSerializer
from rest_framework import mixins
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from django_pandas.io import read_frame
from geopandas import GeoDataFrame, GeoSeries, overlay
from shapely.geometry import Point, Polygon

import numpy as np
import pandas as pd
import geopandas as gpd
import glob, os


class CoronaAppList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = CoronaApp.objects.all()
    serializer_class = CoronaAppSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CoronaAppDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = CoronaApp.objects.all()
    serializer_class = CoronaAppSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CoronaAppResult(APIView):

    def get(self, request, format=None):
        data = CoronaApp.objects.all()
        data_frame = read_frame(data)            # Transform queryset into pandas dataframe 
        data_frame.rename(columns={'name': 'UUID', 'status': 'Status', 'latitude': 'Lat', 'longitude': 'Lng'}, inplace=True)
        data_frame.drop(['id', 'created'], axis=1)

        # ISSUE DETECTED IN 89: drop.['Status_1','UUID_1','Lat_1','Lng_1'] NOT FOUND IN AXIS. UNCOMMENT FOLLOWING LINES ONCE ERROR RESOLVED
        #infected = self.intersection_calculator(data_frame)
        #return Response(infected)


        return Response(data_frame)              # Return the result in JSON via Django REST Framework

    def intersection_calculator(self, data_frame):
        allPts = GeoDataFrame(data_frame,crs={"init":"EPSG:4326"},geometry=[Point(xy) for xy in zip(data_frame["Lat"], data_frame["Lng"])]).to_crs("EPSG:3395")
        positivePoints = allPts[allPts['Status']==1]
        negativePoints = allPts[allPts['Status']==0]

        #print(positivePoints)
        #print(negativePoints)

        positivePointsBuffered = positivePoints.set_geometry(positivePoints.geometry.buffer(20,resolution=16),inplace=False)
        negativePointsBuffered = negativePoints.set_geometry(negativePoints.geometry.buffer(20,resolution=16),inplace=False)
        #print(positivePointsBuffered)

        #ax=positivePointsBuffered.plot(color="red")
        #negativePointsBuffered.plot(ax=ax,color='green', alpha=0.5)

        #intersecting_points = negativePoints.intersection(positivePointsBuffered.unary_union)
        #print(intersecting_points)
        #print(negativePoints)

        #print(negativePoints.loc[negativePoints['geometry'].isin(intersecting_points.to_numpy())])
        #combined_infectious_points = positivePointGeometryBuffered.unary_union


        res_intersect = overlay(positivePointsBuffered,negativePointsBuffered,how='intersection')
        res_intersect=res_intersect.drop(['Status_1','UUID_1','Lat_1','Lng_1','geometry'])
        res_intersect.rename(columns={'Status_2':'Status',
                          'UUID_2':'UUID',
                          'Lat_2':'Lat',
                          'Lng_2':'Lng'},inplace=True)
        #res_intersect['UUID_2'],res_intersect['Status_2']
        res_intersect.drop_duplicates(subset ="UUID",keep = "first", inplace = True)
        res_intersect['Timeslot']=timestamp_string
        return res_intersect


User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Infos successfully updated")
        )
        return super().form_valid(form)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()
