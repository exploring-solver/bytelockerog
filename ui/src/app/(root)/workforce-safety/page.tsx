import { 
  HardHat, Flame, AlertTriangle, Construction, 
  ClipboardCheck, LibraryBig, CaseSensitive
} from 'lucide-react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Image from 'next/image';

// Page 4: Workforce Safety Monitor
export default function WorkforceSafety() {
  return (
    <section className="py-12 px-4 max-w-6xl mx-auto">
      <div className="text-center mb-16">
        <Construction className="mx-auto h-12 w-12 text-blue-600" />
        <h2 className="mt-4 text-3xl font-bold">AI-Powered Workforce Safety Monitoring</h2>
        <p className="mt-2 text-muted-foreground">Preventing accidents before they happen</p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        <Card className="p-6">
          <HardHat className="h-8 w-8 text-orange-500" />
          <h3 className="mt-4 text-xl font-semibold">PPE Compliance</h3>
          <p className="mt-2 text-muted-foreground">
            Real-time detection of safety gear usage including helmets, gloves, and goggles
          </p>
        </Card>

        <Card className="p-6">
          <Flame className="h-8 w-8 text-red-500" />
          <h3 className="mt-4 text-xl font-semibold">Hazard Detection</h3>
          <p className="mt-2 text-muted-foreground">
            Instant alerts for fire risks, chemical leaks, and unsafe material handling
          </p>
        </Card>

        <Card className="p-6">
          <AlertTriangle className="h-8 w-8 text-yellow-500" />
          <h3 className="mt-4 text-xl font-semibold">Accident Prediction</h3>
          <p className="mt-2 text-muted-foreground">
            Machine learning models predicting high-risk scenarios based on historical data
          </p>
        </Card>
      </div>

      <div className="mt-12 grid lg:grid-cols-2 gap-8 items-center">
        <Image 
          src="/safety-demo.jpg"
          alt="Safety Monitoring Demo"
          width={600}
          height={400}
          className="rounded-lg border"
        />
        <div>
          <h3 className="text-2xl font-bold">Key Features</h3>
          <ul className="mt-4 space-y-4">
            <li className="flex items-center gap-2">
              <ClipboardCheck className="h-5 w-5 text-green-500" />
              Compliance rate tracking
            </li>
            <li className="flex items-center gap-2">
              <CaseSensitive className="h-5 w-5 text-blue-500" />
              OSHA standards alignment
            </li>
            <li className="flex items-center gap-2">
              <LibraryBig className="h-5 w-5 text-purple-500" />
              Automated safety reports
            </li>
          </ul>
          <Button className="mt-8">Request Industrial Demo</Button>
        </div>
      </div>
    </section>
  );
}

