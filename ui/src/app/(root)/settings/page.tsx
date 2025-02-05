/* eslint-disable @typescript-eslint/no-unused-vars */
"use client";

import { useState } from "react";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function SettingsPage() {
  const [crowdManagementEnabled, setCrowdManagementEnabled] = useState(false);
  const [crimePreventionEnabled, setCrimePreventionEnabled] = useState(false);
  const [workMonitoringEnabled, setWorkMonitoringEnabled] = useState(false);
  const [alertThreshold, setAlertThreshold] = useState(50);
  const [suspiciousActivitySensitivity, setSuspiciousActivitySensitivity] = useState(70);
  const [restrictedZones, setRestrictedZones] = useState(["Warehouse", "Vault Room"]);
  const [riskyBehaviors, setRiskyBehaviors] = useState(["No Helmet", "Unauthorized Equipment Use"]);

  return (
    <div className="container mx-auto p-6 space-y-6 w-full">
      <h1 className="text-3xl font-bold text-center mb-6">CCTV AI/ML Settings</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Crowd Management Section */}
        <Card>
          <CardHeader>
            <CardTitle>Crowd Management</CardTitle>
            <CardDescription>Configure settings for crowd monitoring.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <Label htmlFor="crowd-management">Enable Crowd Management</Label>
              <Switch id="crowd-management" checked={crowdManagementEnabled} onCheckedChange={setCrowdManagementEnabled} />
            </div>
            {crowdManagementEnabled && (
              <div>
                <Label className="mb-2">Overcrowding Alert Threshold:</Label>
                <Slider defaultValue={[alertThreshold]} max={100} step={1} onValueChange={(value) => setAlertThreshold(value[0])} />
                <p className="mt-2 text-sm text-gray-500">Threshold: {alertThreshold}%</p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Crime Prevention Section */}
        <Card>
          <CardHeader>
            <CardTitle>Crime Prevention</CardTitle>
            <CardDescription>Detect and prevent suspicious activities.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <Label htmlFor="crime-prevention">Enable Crime Prevention</Label>
              <Switch id="crime-prevention" checked={crimePreventionEnabled} onCheckedChange={setCrimePreventionEnabled} />
            </div>
            {crimePreventionEnabled && (
              <>
                <Label className="mb-2">Suspicious Activity Sensitivity:</Label>
                <Slider defaultValue={[suspiciousActivitySensitivity]} max={100} step={1} onValueChange={(value) => setSuspiciousActivitySensitivity(value[0])} />
                <p className="mt-2 text-sm text-gray-500">Sensitivity: {suspiciousActivitySensitivity}%</p>

                <Label className="mt-4 mb-2">Restricted Zones:</Label>
                <div className="space-y-2">
                  {restrictedZones.map((zone, index) => (
                    <p key={index} className="text-gray-700 bg-gray-200 rounded-md p-2">{zone}</p>
                  ))}
                  <Input placeholder="Add New Zone" className="w-full" />
                </div>
              </>
            )}
          </CardContent>
        </Card>

        {/* Work Monitoring Section */}
        <Card>
          <CardHeader>
            <CardTitle>Work Monitoring</CardTitle>
            <CardDescription>Enhance workplace safety and efficiency.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <Label htmlFor="work-monitoring">Enable Work Monitoring</Label>
              <Switch id="work-monitoring" checked={workMonitoringEnabled} onCheckedChange={setWorkMonitoringEnabled} />
            </div>
            {workMonitoringEnabled && (
              <>
                <Label className="mb-2">Risky Behaviors:</Label>
                <div className="space-y-2">
                  {riskyBehaviors.map((behavior, index) => (
                    <p key={index} className="text-gray-700 bg-gray-200 rounded-md p-2">{behavior}</p>
                  ))}
                  <Input placeholder="Add Behavior Rule" className="w-full" />
                </div>
              </>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Save Button */}
      <div className="text-center">
        <Button className="px-6 py-3 text-lg">Save Settings</Button>
      </div>
    </div>
  );
}
