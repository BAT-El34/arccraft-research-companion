import '../../globals.css';
export default async function Layout({children,params}:{children:React.ReactNode;params:Promise<{locale:string}>}) {
  const {locale}=await params;
  return <html lang={locale} suppressHydrationWarning><head><script dangerouslySetInnerHTML={{__html:"try{document.documentElement.dataset.theme=localStorage.getItem('arccraft-theme')||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light')}catch(e){}"}}/></head><body>{children}</body></html>
}
