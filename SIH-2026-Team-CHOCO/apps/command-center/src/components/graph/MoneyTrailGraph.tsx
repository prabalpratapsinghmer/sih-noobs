import { useEffect, useRef, useState } from 'react';
import { Network } from 'vis-network';
import { DataSet } from 'vis-data';

export function MoneyTrailGraph({ complaintId }: { complaintId: string }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const networkRef = useRef<Network | null>(null);

  useEffect(() => {
    if (!containerRef.current || !complaintId) return;

    fetch(`/api/v1/victim/intelligence/${complaintId}`)
      .then(res => res.json())
      .then(intelligence => {
        if (!intelligence || !intelligence.mule_nodes) return;

        // Use our CSS custom properties from the shared Tailwind design system
        const colorLine = getComputedStyle(document.documentElement).getPropertyValue('--line').trim() || '#31405f';
        const colorCrit = getComputedStyle(document.documentElement).getPropertyValue('--crit').trim() || '#f0697c';
        const colorWarn = getComputedStyle(document.documentElement).getPropertyValue('--warn').trim() || '#e3a34b';
        const colorGood = getComputedStyle(document.documentElement).getPropertyValue('--good').trim() || '#3ecf9c';
        const colorInk = getComputedStyle(document.documentElement).getPropertyValue('--ink').trim() || '#ffffff';

        // Build dynamic nodes and edges based on intelligence payload
        const dynamicNodes = [];
        const dynamicEdges = [];
        
        // 1. Victim Node
        dynamicNodes.push({
          id: 'V1',
          label: `Victim\n₹${intelligence.amount || 0}`,
          group: 'victim',
          title: `Lost ₹${intelligence.amount || 0} (${intelligence.victim_name || 'Unknown'})`
        });

        // 2. Mule Nodes & Edges from Victim
        intelligence.mule_nodes.forEach((mule: any, i: number) => {
          const riskGroup = mule.risk_score > 0.85 ? 'mule_high' : 'mule_low';
          dynamicNodes.push({
            id: mule.id,
            label: `${mule.bank.split(' ')[0]}\n${(mule.risk_score * 100).toFixed(0)}% Risk`,
            group: riskGroup,
            title: `Account: ${mule.account}\nRisk Score: ${(mule.risk_score * 100).toFixed(1)}%\nTier: ${mule.tier}`
          });
          
          // Edge from Victim to Mule (we pretend they all originate from V1 for visualization)
          dynamicEdges.push({
            from: 'V1',
            to: mule.id,
            label: `₹${mule.amount || 0}`,
            arrows: 'to'
          });
        });

        // 3. ATM Nodes & Edges from high-risk mules
        if (intelligence.atms) {
          intelligence.atms.forEach((atm: any, i: number) => {
            if (atm.risk_score > 0.8) {
               dynamicNodes.push({
                 id: atm.atm_id,
                 label: `${atm.atm_id}\nCash-out Risk`,
                 group: 'atm_high',
                 title: `${atm.name}\nETA: ${atm.eta_min} min\nPatrol: ${atm.assigned_patrol}`
               });
               
               // Connect high-risk mules to ATMs to show cash-out vectors
               const highRiskMules = intelligence.mule_nodes.filter((m: any) => m.risk_score > 0.85);
               if (highRiskMules.length > 0) {
                 const sourceMule = highRiskMules[i % highRiskMules.length];
                 dynamicEdges.push({
                   from: sourceMule.id,
                   to: atm.atm_id,
                   label: 'Cash-out',
                   arrows: 'to',
                   dashes: true
                 });
               }
            }
          });
        }

        const data: any = {
          nodes: new DataSet(dynamicNodes as any),
          edges: new DataSet(dynamicEdges as any)
        };

        const options: any = {
          autoResize: true,
          nodes: {
            shape: 'dot',
            size: 20,
            font: { color: colorInk, size: 14, multi: true, bold: '14px' },
            borderWidth: 2,
            shadow: true,
          },
          edges: {
            width: 2,
            color: { color: colorLine, highlight: colorCrit },
            font: { color: colorInk, size: 12, align: 'top' },
            smooth: { enabled: true, type: 'continuous' }
          },
          groups: {
            victim: { color: { background: colorGood, border: colorGood } },
            mule_high: { color: { background: colorCrit, border: colorCrit } },
            mule_low: { color: { background: colorWarn, border: colorWarn } },
            atm_high: { shape: 'square', color: { background: colorCrit, border: colorCrit } },
          },
          physics: {
            forceAtlas2Based: {
              gravitationalConstant: -50,
              centralGravity: 0.01,
              springLength: 100,
              springConstant: 0.08
            },
            maxVelocity: 50,
            solver: 'forceAtlas2Based',
            timestep: 0.35,
            stabilization: { iterations: 150 }
          },
          interaction: {
            hover: true,
            tooltipDelay: 200,
            zoomView: true
          }
        };

        if (networkRef.current) {
          networkRef.current.destroy();
        }
        networkRef.current = new Network(containerRef.current!, data, options);
      })
      .catch(err => console.error("Failed to load intelligence graph:", err));

    return () => {
      networkRef.current?.destroy();
    };
  }, [complaintId]);

  return (
    <div className="w-full h-full relative">
      <div 
        ref={containerRef} 
        className="w-full h-full absolute inset-0 cursor-grab active:cursor-grabbing" 
      />
    </div>
  );
}
