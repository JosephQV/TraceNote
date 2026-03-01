/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 */

import { NewAppScreen } from '@react-native/new-app-screen';
import { StatusBar, StyleSheet, Text, useColorScheme, View } from 'react-native';

import React from 'react';
import AppNavigator from './src/navigation/appnav';

export default function App() {
  return <AppNavigator />;
}