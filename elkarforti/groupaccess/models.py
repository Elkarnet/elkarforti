from django.db import models
from django.forms import ModelForm
from django.urls import reverse

import pyfortiapi
from Crypto.Cipher import AES # https://nitratine.net/blog/post/python-encryption-and-decryption-with-pycryptodome/
from Crypto.Random import get_random_bytes
from django.core.exceptions import ValidationError

import os.path
from os import path

# Create your models here.

from django.db import models


class FortiParameters(models.Model):
    fortiIP = models.CharField(max_length=16)
    fortiPort = models.IntegerField(default=443)
    fortiVdom = models.CharField(max_length=32)
    fortiUserName = models.CharField(max_length=32)
    fortiPassword = models.CharField(max_length=128)
    fortiDefaultGroupName = models.CharField(max_length=32)
    fortiAccessEnabledGroupName = models.CharField(max_length=32)
    fortiKeyStorePath = models.CharField(max_length=128,default="/etc/elkarforti/")
    automaticOpenClose = models.BooleanField(default=True)
    automaticOpenTime = models.TimeField(default = "15:00" )
    automaticCloseTime = models.TimeField(default = "22:00" )

    def save(self, *args, **kwargs):
        data = self.fortiPassword.encode('utf8')

        keypath = self.fortiKeyStorePath+"/key.bin"
        if not(path.exists(keypath)):
            # Generate the key
            key = get_random_bytes(16)
            # Save the key to a file
            file_out = open(keypath, "wb") # wb = write bytes
            file_out.write(key)
            file_out.close()

        file_in =  open(keypath,"rb")
        key_from_file = file_in.read()
        file_in.close()
        cipher = AES.new(key_from_file, AES.MODE_CFB)
        ciphered_data = cipher.encrypt(data)
        encryptedpath = self.fortiKeyStorePath+"/encrypted.bin"
        file_out = open(encryptedpath, "wb")
        file_out.write(cipher.iv)
        file_out.write(ciphered_data)
        file_out.close()

        self.fortiPassword = 'encrypted'

        super().save(*args, **kwargs)  # Call the "real" save() method.

    @property
    def getEncrypted(self):
        configRecord = FortiParameters.objects.get(pk=1)
        fortiKeyStorePath = configRecord.fortiKeyStorePath
        keypath = fortiKeyStorePath+"/key.bin"
        encryptedpath = fortiKeyStorePath+"/encrypted.bin"
        file_in =  open(keypath,"rb")
        key_from_file = file_in.read()
        file_in.close()

        file_in =  open(encryptedpath,"rb")
        iv = file_in.read(16)
        ciphered_data = file_in.read()
        file_in.close()
        cipher = AES.new(key_from_file, AES.MODE_CFB, iv=iv)
        original_data = cipher.decrypt(ciphered_data)
        original_data = original_data.decode('utf8')
        print('------------ ORIGINAL PASS -----------------')
        print(original_data)
        return original_data



class FortiGroup(models.Model):
    name = models.CharField(max_length=200)
    enabled = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('index.html', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):

        parameters = FortiParameters.objects.get(id=1)
        device = pyfortiapi.FortiGate(ipaddr=parameters.fortiIP, username=parameters.fortiUserName, password= parameters.getEncrypted, port=parameters.fortiPort, vdom=parameters.fortiVdom)

        my_group   = device.get_address_group(self.name)
        my_address = device.get_firewall_address(self.name)

        if ((my_group == 404) and (my_address == 404)):
            raise ValidationError("The group name does not exists on Forti")


        super().save(*args, **kwargs)  # Call the "real" save() method.

        all_enabled_groups = FortiGroup.objects.filter(enabled=True)
        defaultGroupName = parameters.fortiDefaultGroupName  # Talde huts bat ez du Fortik onartzen
        payload_list=[]
        dict_gela = {'name':defaultGroupName}
        payload_list.append(dict_gela)

        for group in all_enabled_groups:
            dict_gela = {'name':group.name}
            payload_list.append(dict_gela)
            print("payload_list: ", payload_list)

        payload = "{{'member': {} }}".format(payload_list)
        device.update_address_group(parameters.fortiAccessEnabledGroupName, payload)

    def __str__(self):
           return self.name



class FortiGroupForm(ModelForm):
    class Meta:
        model = FortiGroup
        fields = ['name', 'enabled']
