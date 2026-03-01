
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

import LandingScreen from '../screens/landing';
import SignupScreen from '../screens/signup';
import LoginScreen from '../screens/login';
import HomeScreen from '../screens/home';
import CreatePostScreen from '../screens/createposts';
import CreateProfileScreen from '../screens/createpf';
import ViewProfileScreen from '../screens/viewpf';


export type RootStackParamList = {
  Landing: undefined;
  Signup: undefined;
  Home: undefined;
  Login: undefined;
  CreatePost: undefined;
  CreateProfile: undefined;
  ViewProfile: undefined;

};

const Stack = createNativeStackNavigator<RootStackParamList>();

const AppNavigator = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Landing">
        <Stack.Screen name="Landing" component={LandingScreen} />
        <Stack.Screen name="Signup" component={SignupScreen} />
        <Stack.Screen name="Login" component={LoginScreen} />
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="CreatePost" component={CreatePostScreen} />
         <Stack.Screen name="CreateProfile" component={CreateProfileScreen} />
        <Stack.Screen name="ViewProfile" component={ViewProfileScreen} /> 
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default AppNavigator;