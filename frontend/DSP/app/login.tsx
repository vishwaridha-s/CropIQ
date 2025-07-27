import { ImageBackground,Image, ScrollView, StyleSheet, Text, View, TextInput, Button, StatusBar } from 'react-native';
import { Stack, Link, useRouter } from 'expo-router';
import React, { useState } from 'react';
import axios from 'axios';

const Login = () => {
  const [Name, setName] = useState('');
  const [Password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const router = useRouter();

  const handleLogin = async () => {
    const data = {
      username: Name,
      password: Password,
    };

    try {
      // Ensure the query parameter action=login is present in the URL
      const response = await axios.post("http://192.168.95.237/user/?action=login", data);
      
      if (response.data.status === 200 || response.data.message === "Login successful!") {
        router.push("/Home");
      } else {
        setMessage("Login failed");
      }
    } catch (error) {
      console.log("Login failed:", error.response?.data || error);
      setMessage("Failed, please try again");
    }
  };

  return (
    <>
      <Stack.Screen options={{ headerShown: false }} />
      <StatusBar backgroundColor="#77bba2" />
      <ImageBackground
        source={require("@/assets/images/Appbg.png")}
        style={styles.Background}
      >
        <ScrollView>
          <View style={styles.container}>
           <View style={styles.logoContainer}>
                       <Image source={require('../assets/images/logo.png')} style={styles.logo} />
              </View>

            <View style={styles.Login}>
              <Text style={{ fontSize: 40, textAlign: "center" }}>Login</Text>

              <TextInput
                value={Name}
                onChangeText={(text) => setName(text)}
                placeholder="Enter Your UserName"
                style={styles.input}
              />

              <TextInput
                value={Password}
                onChangeText={(text) => setPassword(text)}
                placeholder="Enter Your Password"
                secureTextEntry
                style={styles.input}
              />

              <Button color="black" title="Login" onPress={handleLogin} />

              {/* Display message */}
              {message !== '' && (
                <Text style={{ color: "red", textAlign: "center", marginTop: 10 }}>{message}</Text>
              )}

      
              <Link href=" ">
                <Text style={styles.linkText}>Forgot Password?</Text>
              </Link>

              {/* New User and SignUp in one line */}
              <View style={styles.row}>
                <Text style={styles.text}>New User? </Text>
                <Link href="/">
                  <Text style={styles.signupLink}>SignUp</Text>
                </Link>
              </View>
            </View>
          </View>
        </ScrollView>
      </ImageBackground>
    </>
  );
};

export default Login;

const styles = StyleSheet.create({
  Background: {
    height: "100%",
    width: "100%",
    resizeMode: "cover",
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
  container: {
    flex: 1,
    flexDirection: "column",
    gap: 70,
    margin: 20,
  },
  Login: {
    flex: 1,
    flexDirection: "column",
    gap: 24,
  },
  input: {
    borderRadius: 10,
    padding: 16,
    backgroundColor: "#77bba2",
  },
  linkText: {
    color: "blue",
    textDecorationLine: "underline",
    fontSize: 17,
    textAlign: "center",
  },
  row: {
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    gap: 4,
  },
  text: {
    fontSize: 17,
  },
  signupLink: {
    color: "blue",
    fontSize: 17,
    textDecorationLine: "underline",
  },
});