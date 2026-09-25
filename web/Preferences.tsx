'use client';
import {useEffect,useState} from 'react';
import {Locale,tr} from './i18n';
export default function Preferences({locale}:{locale:Locale}) {
  const [dark,setDark]=useState(false);
  useEffect(()=>{setDark(document.documentElement.dataset.theme==='dark');},[]);
  return <button className="theme-button" onClick={()=>{const value=!dark;setDark(value);document.documentElement.dataset.theme=value?'dark':'light';try{localStorage.setItem('arccraft-theme',value?'dark':'light');}catch{}}} aria-pressed={dark}>{dark?'◐':'◑'} {tr(locale,'Theme','Thème')}</button>;
}
