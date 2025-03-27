"use client";

import Image from "next/image";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Progress } from "@/components/ui/progress";
import { Card, CardContent } from "@/components/ui/card";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";

export default function Home() {
  const [step, setStep] = useState(1);
  const [files, setFiles] = useState([]);
  const [parsedText, setParsedText] = useState("");
  const [metadata, setMetadata] = useState({ institution: '', docType: '', year: '' });
  const [chunks, setChunks] = useState([]);
  const [entities, setEntities] = useState([]);
  const [triplets, setTriplets] = useState([]);

  const handleNext = () => setStep(step + 1);
  const handleBack = () => setStep(step - 1);

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start w-full max-w-5xl">
        <Image
          className="dark:invert"
          src="/next.svg"
          alt="Next.js logo"
          width={180}
          height={38}
          priority
        />

        <Progress value={(step / 7) * 100} className="w-full" />

        <Tabs defaultValue={`step${step}`} className="w-full">
          <TabsList className="grid grid-cols-7 mb-6">
            {[...Array(7)].map((_, i) => (
              <TabsTrigger key={i} value={`step${i + 1}`}>Step {i + 1}</TabsTrigger>
            ))}
          </TabsList>

          <TabsContent value="step1">
            <Card>
              <CardContent className="space-y-4">
                <h2 className="text-xl font-semibold">1. Upload Documents</h2>
                <Input type="file" multiple onChange={(e) => setFiles([...e.target.files])} />
                <Button onClick={handleNext}>Next</Button>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="step2">
            <Card>
              <CardContent className="space-y-4">
                <h2 className="text-xl font-semibold">2. Text Parsing</h2>
                <Textarea placeholder="Parsed text will appear here..." value={parsedText} onChange={(e) => setParsedText(e.target.value)} />
                <div className="flex justify-between">
                  <Button onClick={handleBack}>Back</Button>
                  <Button onClick={handleNext}>Next</Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="step3">
            <Card>
              <CardContent className="space-y-4">
                <h2 className="text-xl font-semibold">3. Metadata Tagging</h2>
                <Input placeholder="Institution" value={metadata.institution} onChange={(e) => setMetadata({ ...metadata, institution: e.target.value })} />
                <Input placeholder="Document Type" value={metadata.docType} onChange={(e) => setMetadata({ ...metadata, docType: e.target.value })} />
                <Input placeholder="Year" value={metadata.year} onChange={(e) => setMetadata({ ...metadata, year: e.target.value })} />
                <div className="flex justify-between">
                  <Button onClick={handleBack}>Back</Button>
                  <Button onClick={handleNext}>Next</Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="step4">
            <Card>
              <CardContent className="space-y-4">
                <h2 className="text-xl font-semibold">4. Text Chunking</h2>
                <Textarea placeholder="Chunks will appear here..." value={chunks.join('\n\n')} onChange={(e) => setChunks(e.target.value.split('\n\n'))} rows={8} />
                <div className="flex justify-between">
                  <Button onClick={handleBack}>Back</Button>
                  <Button onClick={handleNext}>Next</Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="step5">
            <Card>
              <CardContent className="space-y-4">
                <h2 className="text-xl font-semibold">5. Named Entity Recognition</h2>
                <Textarea placeholder="Entities will appear here..." value={entities.join(', ')} onChange={(e) => setEntities(e.target.value.split(','))} rows={4} />
                <div className="flex justify-between">
                  <Button onClick={handleBack}>Back</Button>
                  <Button onClick={handleNext}>Next</Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="step6">
            <Card>
              <CardContent className="space-y-4">
                <h2 className="text-xl font-semibold">6. Triple Extraction</h2>
                <Textarea placeholder="Enter (subject, predicate, object) triples here..." value={triplets.join('\n')} onChange={(e) => setTriplets(e.target.value.split('\n'))} rows={6} />
                <div className="flex justify-between">
                  <Button onClick={handleBack}>Back</Button>
                  <Button onClick={handleNext}>Next</Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="step7">
            <Card>
              <CardContent className="space-y-4">
                <h2 className="text-xl font-semibold">7. Export as JSON</h2>
                <pre className="bg-gray-100 p-4 rounded text-sm overflow-x-auto">
                  {JSON.stringify({ chunks, metadata, entities, triplets }, null, 2)}
                </pre>
                <div className="flex justify-between">
                  <Button onClick={handleBack}>Back</Button>
                  <Button onClick={() => alert('Export complete!')}>Export</Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}
