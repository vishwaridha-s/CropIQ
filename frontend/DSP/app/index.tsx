import { ImageBackground,Image, StyleSheet, Text, TextInput, View, Button, ScrollView, StatusBar } from "react-native";
import { Link, Stack, useRouter } from "expo-router";
import React, { useState } from "react";
import axios from "axios";

const Signup = () => {
  const router = useRouter();

  const [Name, setName] = useState('');
  const [Password, setPassword] = useState('');
  const [ConfirmPassword, setConfirmPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const handleSignup = async () => {
    if (Password !== ConfirmPassword) {
      setErrorMessage("Passwords do not match");
      return;
    }
    setErrorMessage('');

    const data = {
      username: Name,
      password: Password,
    };

    try {
      const response = await axios.post("http://192.168.95.237/user/?action=signup", data);
      
      if (response.data.status === 200 || response.data.message === "Signup successful!") {
        router.push("/login");
      } else {
        setErrorMessage(response.data.message || "Signup failed");
      }
    } catch (error) {
      setErrorMessage("Signup failed. Please try again.");
    }
  };

  return (
    <ImageBackground
      style={styles.Background}
      source={require("@/assets/images/Appbg.png")}
    >
      <ScrollView>
        <View style={styles.container}>
          <Stack.Screen options={{ headerShown: false }} />
          <StatusBar backgroundColor="#77bba2" />

          <View style={styles.logoContainer}>
            <Image source={require('../assets/images/logo.png')} style={styles.logo} />
          </View>

          <View style={styles.SignUp}>
            <Text style={{ textAlign: "center", fontSize: 35 }}>SignUp</Text>

            <TextInput 
              value={Name} 
              onChangeText={(text) => setName(text)} 
              placeholder="UserName" 
              style={styles.input} 
            />
            <TextInput 
              value={Password} 
              onChangeText={(text) => setPassword(text)} 
              placeholder="Password" 
              secureTextEntry 
              style={styles.input} 
            />
            <TextInput 
              value={ConfirmPassword} 
              onChangeText={(text) => setConfirmPassword(text)} 
              placeholder="Confirm Password" 
              secureTextEntry 
              style={styles.input} 
            />

            <View>
              <Button title="SignUp" color="black" onPress={handleSignup} />
            </View>
            {errorMessage !== '' && (
              <Text style={styles.errorText}>{errorMessage}</Text>
            )}

            <View style={styles.Login}>
              <Text style={{ fontSize: 16 }}>Already Have An Account? </Text>
              <Link href="/login">
                <Text style={{ color: "blue", textDecorationLine: "underline", fontSize: 17 }}>
                  Login
                </Text>
              </Link>
            </View>
          </View>
        </View>
      </ScrollView>
    </ImageBackground>
  );
};

export default Signup;

const styles = StyleSheet.create({
  container: {
    margin: 20,
    flex: 1,
    flexDirection: "column",
    gap: 90,
  },
  logo:{
    width:220,
    height:220,
   
  },
  logoContainer:{
    justifyContent:'center',
    alignItems:'center',
    marginTop:-10,
  },
  Background: {
    height: "100%",
    width: "100%",
    resizeMode: "cover",
  },
  input: {
    marginVertical: 10,
    padding: 16,
    borderRadius: 10,
    backgroundColor: "#77bba2",
  },
  Login: {
    flexDirection: "row",
    textAlign: "center",
    alignItems: "center",
    justifyContent: "center",
  },
  SignUp: {
    flex: 1,
    flexDirection: "column",
    gap: 14,
  },
  errorText: {
    color: "red",
    textAlign: "center",
    fontSize: 14,
    marginBottom: 10,
  },
});