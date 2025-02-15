import { 
  LineChart, BadgeCheck, Trophy, CaseSensitive
} from 'lucide-react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Image from 'next/image';

export default function CaseStudies() {
  return (
    <section className="py-16 px-4 max-w-6xl mx-auto">
      <div className="text-center mb-16">
        <Trophy className="mx-auto h-12 w-12 text-yellow-600" />
        <h2 className="mt-4 text-3xl font-bold">Proven Impact in Smart Cities</h2>
        <p className="mt-2 text-muted-foreground">Real-world implementations and measurable results</p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        <Card className="p-6">
          <div className="flex items-center gap-2 mb-4">
            <BadgeCheck className="h-6 w-6 text-green-500" />
            <h3 className="text-xl font-semibold">Mumbai Smart City</h3>
          </div>
          <ul className="space-y-2 text-muted-foreground">
            <li>32% reduction in street crimes</li>
            <li>18% faster emergency response</li>
            <li>₹2.8Cr annual savings</li>
          </ul>
        </Card>

        <Card className="p-6">
          <div className="flex items-center gap-2 mb-4">
            <LineChart className="h-6 w-6 text-blue-500" />
            <h3 className="text-xl font-semibold">Delhi NCR Deployment</h3>
          </div>
          <ul className="space-y-2 text-muted-foreground">
            <li>41% improvement in traffic management</li>
            <li>27% reduction in accidents</li>
            <li>900+ safety violations detected</li>
          </ul>
        </Card>

        <Card className="p-6">
          <div className="flex items-center gap-2 mb-4">
            <CaseSensitive className="h-6 w-6 text-purple-500" />
            <h3 className="text-xl font-semibold">Chennai Industrial Zone</h3>
          </div>
          <ul className="space-y-2 text-muted-foreground">
            <li>94% PPE compliance achieved</li>
            <li>Zero fatal accidents in 18 months</li>
            <li>ISO 45001 certification</li>
          </ul>
        </Card>
      </div>

      <div className="mt-12 grid lg:grid-cols-2 gap-8 items-center">
        <div>
          <h3 className="text-2xl font-bold">ROI Calculator</h3>
          <p className="mt-4 text-muted-foreground">
            Estimate potential savings for your municipality:
          </p>
          <div className="mt-6 space-y-4">
            <div className="flex justify-between items-center">
              <span>Cameras Installed</span>
              <span className="font-semibold">1,250+</span>
            </div>
            <div className="flex justify-between items-center">
              <span>Average Response Improvement</span>
              <span className="font-semibold">37% faster</span>
            </div>
            <div className="flex justify-between items-center">
              <span>Typical Cost Savings</span>
              <span className="font-semibold">₹4.2L/month</span>
            </div>
          </div>
          <Button className="mt-8">Calculate Your Savings</Button>
        </div>
        
        <Image 
          src="/city-map.jpg"
          alt="Smart City Coverage"
          width={600}
          height={400}
          className="rounded-lg border"
        />
      </div>
    </section>
  );
}