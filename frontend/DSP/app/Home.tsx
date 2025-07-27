import {ImageBackground,Image, ScrollView, StyleSheet, Text, View, Alert, TouchableOpacity, StatusBar, TextInput,} from 'react-native';
import * as Location from 'expo-location';
import { Link, Stack, useRouter } from 'expo-router';
import { Picker } from '@react-native-picker/picker';
import React, { useState } from 'react';
import axios from 'axios';

const Home = () => {
  const router = useRouter();

  const [Name, setName] = useState('');
  const [locationGranted, setLocationGranted] = useState(false);
  const [district, setDistrict] = useState('');
  const [state, setState] = useState('');

  const [ipAddress, setIpAddress] = useState('');
  const [latitude, setLatitude] = useState<number | null>(null);
  const [longitude, setLongitude] = useState<number | null>(null);

  const handleGetCrops = async () => {
    if (!Name || !district || !state) {
      Alert.alert('Missing Fields', 'Please fill all fields.');
      return;
    }

    if (!locationGranted) {
      Alert.alert('Location Required', 'Please allow location access.');
      return;
    }

    try {
      const ipResponse = await fetch('https://ipinfo.io/json?token=cf975591a02f51');
      const ipData = await ipResponse.json();
      const ip = ipData.ip;
      setIpAddress(ip);

      const location = await Location.getCurrentPositionAsync({});
      const currentLatitude = location.coords.latitude;
      const currentLongitude = location.coords.longitude;
      setLatitude(currentLatitude);
      setLongitude(currentLongitude);

      const data = {
        District: district,
        state: state,
        ip: ip,
        latitude: currentLatitude,
        longitude: currentLongitude,
      };

      const response = await axios.post("http://192.168.95.237/submit-location/", data);

      // 🔽 Printing and alerting status and message
      console.log("Backend Response:", response.data);

      const { status, message } = response.data;

      if (message==="Coordinates received and analyzed successfully.") {
        Alert.alert('Success', message || 'Data submitted successfully!');
        router.push('/output');
      } else {
        Alert.alert('Error', message || 'An error occurred. Please try again.');
      }
    } catch (error) {
      console.log('An error occurred', error);
      Alert.alert('Network Error', 'Unable to reach server.');
    }
  };

  const requestLocationPermission = async () => {
    const { status } = await Location.requestForegroundPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Permission needed', 'Location access is required');
      return;
    }
    setLocationGranted(true);
    Alert.alert('Success', 'Location permission granted');
  };

  return (
    <>
      <Stack.Screen options={{ headerShown: false }} />
      <StatusBar backgroundColor="#77bba2" />
      <ImageBackground
        source={require("@/assets/images/Appbg.png")}
        style={styles.Background}
      >
        <View style={styles.logoContainer}>
                               <Image source={require('../assets/images/logo.png')} style={styles.logo} />
                      </View>
        <ScrollView>
          <View style={styles.container}>
            <TextInput
              value={Name}
              onChangeText={setName}
              placeholder="Enter your name"
              style={styles.input}
            />

            <View style={styles.pickerContainer}>
              <Text style={styles.label}>Select District:</Text>
              <Picker
                selectedValue={district}
                onValueChange={(value) => setDistrict(value)}
                style={styles.picker}
              >
                <Picker.Item label="Select District" value="" />
                <Picker.Item label="Ariyalur" value="Ariyalur" />
                <Picker.Item label="Chengalpattu" value="Chengalpattu" />
                <Picker.Item label="Chennai" value="Chennai" />
                <Picker.Item label="Coimbatore" value="Coimbatore" />
                <Picker.Item label="Cuddalore" value="Cuddalore" />
                <Picker.Item label="Dharmapuri" value="Dharmapuri" />
                <Picker.Item label="Dindigul" value="Dindigul" />
                <Picker.Item label="Erode" value="Erode" />
                <Picker.Item label="Kallakurichi" value="Kallakurichi" />
                <Picker.Item label="Kancheepuram" value="Kancheepuram" />
                <Picker.Item label="Karur" value="Karur" />
                <Picker.Item label="Krishnagiri" value="Krishnagiri" />
                <Picker.Item label="Madurai" value="Madurai" />
                <Picker.Item label="Mayiladuthurai" value="Mayiladuthurai" />
                <Picker.Item label="Nagapattinam" value="Nagapattinam" />
                <Picker.Item label="Namakkal" value="Namakkal" />
                <Picker.Item label="Nilgiris" value="Nilgiris" />
                <Picker.Item label="Perambalur" value="Perambalur" />
                <Picker.Item label="Pudukkottai" value="Pudukkottai" />
                <Picker.Item label="Ramanathapuram" value="Ramanathapuram" />
                <Picker.Item label="Ranipet" value="Ranipet" />
                <Picker.Item label="Salem" value="Salem" />
                <Picker.Item label="Sivaganga" value="Sivaganga" />
                <Picker.Item label="Tenkasi" value="Tenkasi" />
                <Picker.Item label="Thanjavur" value="Thanjavur" />
                <Picker.Item label="Theni" value="Theni" />
                <Picker.Item label="Thiruvallur" value="Thiruvallur" />
                <Picker.Item label="Thiruvarur" value="Thiruvarur" />
                <Picker.Item label="Thoothukudi" value="Thoothukudi" />
                <Picker.Item label="Tiruchirappalli" value="Tiruchirappalli" />
                <Picker.Item label="Tirunelveli" value="Tirunelveli" />
                <Picker.Item label="Tirupathur" value="Tirupathur" />
                <Picker.Item label="Tiruppur" value="Tiruppur" />
                <Picker.Item label="Tiruvannamalai" value="Tiruvannamalai" />
                <Picker.Item label="Vellore" value="Vellore" />
                <Picker.Item label="Viluppuram" value="Viluppuram" />
                <Picker.Item label="Virudhunagar" value="Virudhunagar" />
              </Picker>
            </View>

            <View style={styles.pickerContainer}>
              <Text style={styles.label}>Select State:</Text>
              <Picker
                selectedValue={state}
                onValueChange={(value) => setState(value)}
                style={styles.picker}
              >
                <Picker.Item label="Select State" value="" />
                <Picker.Item label="Tamil Nadu" value="Tamil Nadu" />
              </Picker>
            </View>

            <View style={styles.ButtonContainer}>
              <TouchableOpacity
                style={styles.Button}
                onPress={requestLocationPermission}
              >
                <Text style={styles.ButtonText}>ALLOW LOCATION</Text>
              </TouchableOpacity>
            </View>

            <View style={styles.ButtonContainer}>
              <TouchableOpacity
                style={styles.GetCropsButton}
                onPress={handleGetCrops}
              >
                <Text style={styles.ButtonText1}>Get Crops</Text>
              </TouchableOpacity>
            </View>
          </View>
        </ScrollView>
      </ImageBackground>
    </>
  );
};

export default Home;

const styles = StyleSheet.create({
  Background: {
    height: '100%',
    width: '100%',
    resizeMode: 'cover',
  },
  logo:{
    width:220,
    height:220,
   
  },
  logoContainer:{
    justifyContent:'center',
    alignItems:'center',
    marginTop:10
  },
  container: {
    margin: 20,
    flex: 1,
    gap: 15,
    marginTop: 80,
  },
  input: {
    borderRadius: 10,
    padding: 18,
    backgroundColor: '#77bba2',
    color:'black'
  },
  pickerContainer: {
    backgroundColor: '#77bba2',
    borderRadius: 8,
    marginVertical: 10,
  },
  picker: {
    height: 50,
    width: '100%',
  },
  label: {
    fontSize: 16,
    paddingLeft: 10,
    paddingTop: 5,
    fontWeight: 'bold',
  },
  ButtonContainer: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  Button: {
    padding: 16,
    paddingLeft: 70,
    paddingRight: 70,
    backgroundColor: '#77bba2',
    borderRadius: 7,
  },
  GetCropsButton: {
    borderWidth: 1,
    padding: 16,
    paddingLeft: 70,
    paddingRight: 70,
    backgroundColor: 'black',
    borderRadius: 7,
  },
  ButtonText: {
    fontSize: 15,
    color: 'white',
    fontWeight: 'bold',
  },
  ButtonText1: {
    fontSize: 17,
    color: 'white',
    fontWeight: 'bold',
  },
});
