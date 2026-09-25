'use client';
import {useEffect,useState} from 'react';
import {Locale,tr} from './i18n';
export default function Health({locale}:{locale:Locale}) {
  const [health,setHealth]=useState<Record<string,unknown>|null>(null);const [error,setError]=useState(false);
  useEffect(()=>{const c=new AbortController();fetch('/api/v1/health',{signal:c.signal}).then(r=>{if(!r.ok)throw Error();return r.json()}).then(setHealth).catch(()=>{if(!c.signal.aborted)setError(true)});return ()=>c.abort()},[]);
  return <section className="panel"><h2>{tr(locale,'Runtime identity','Identité du runtime')}</h2><div role="status">{error?tr(locale,'API unavailable. Static evidence remains accessible.','API indisponible. Les preuves statiques restent accessibles.'):health?<><p>{health.status==='ok'?'✓':'!'} {tr(locale,'Engine integrity','Intégrité du moteur')} : {String(health.status)}</p><p>{tr(locale,'Live computation','Calcul en direct')} : {health.live_computation?tr(locale,'available','disponible'):tr(locale,'awaiting shared rate-limit qualification','en attente de qualification du contrôle de débit partagé')}</p><dl><dt>{tr(locale,'Build commit','Commit du build')}</dt><dd><code>{String(health.build_commit)}</code></dd><dt>{tr(locale,'Science commit','Commit scientifique')}</dt><dd><code>{String(health.science_commit)}</code></dd></dl><details><summary>{tr(locale,'Complete health record','État de santé complet')}</summary><pre>{JSON.stringify(health,null,2)}</pre></details></>:tr(locale,'Checking runtime…','Vérification du runtime…')}</div></section>
}
