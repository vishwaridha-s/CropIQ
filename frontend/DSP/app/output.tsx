import { Stack } from 'expo-router';
import React, { useEffect, useState } from 'react';
import { StyleSheet, Text, View, SafeAreaView, FlatList } from 'react-native';
import { StatusBar } from 'react-native';
import { ImageBackground } from 'react-native';
const Output = () => {
  const [data, setData] = useState({
    rice_varieties: [],
    top_crops: []
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://192.168.95.237/predict-crop/');
        const result = await response.json();
        setData(result);
      } catch (error) {
        console.error('Error fetching crop data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <>
    <Stack.Screen options={{ headerShown: false }} />
      <StatusBar backgroundColor="#77bba2" />
      <ImageBackground
              source={require("@/assets/images/Appbg1.png")}
              style={styles.Background}
            >
              <View style={styles.container}>
      <Text style={styles.title}>🌾 Recommended Rice Varieties</Text>
      {(data.rice_varieties || []).map((variety, index) => (
        <Text key={index} style={styles.variety}>{variety}</Text>
      ))}

      <Text style={styles.title}>🥗 Top 5 Crop Suggestions</Text>
      <FlatList
        data={data.top_crops || []}
        keyExtractor={(_, index) => index.toString()}
        renderItem={({ item }) => (
          <View style={styles.cropRow}>
            <Text style={styles.cropName}>{item[0]}</Text>
            <Text style={styles.cropScore}>{(item[1]).toFixed(2)}%</Text>
          </View>
        )}

      />
      </View>
      </ImageBackground>
      </>
  );
};

export default Output;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding:20,
  },
  Background: {
    height: '100%',
    width: '100%',
    resizeMode: 'contain',
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    marginVertical: 10,
    color: '#333'
  },
  variety: {
    fontSize: 18,
    color: '#007f5f',
    marginBottom: 5
  },
  cropRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    backgroundColor: '#fff',
    padding: 15,
    marginVertical: 5,
    borderRadius: 10,
    elevation: 2
  },
  cropName: {
    fontSize: 18,
    color: '#333'
  },
  cropScore: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#555'
  }
});
