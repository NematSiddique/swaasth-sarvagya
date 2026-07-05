import { createFileRoute } from "@tanstack/react-router"

import { hospitals, modules } from "@/components/HealSync/data"
import { ScoreBar, StatusBadge } from "@/components/HealSync/status"
import { Badge } from "@/components/ui/badge"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

export const Route = createFileRoute("/_layout/operations")({
  component: OperationsPage,
  head: () => ({
    meta: [{ title: "Operations | HealSync AI" }],
  }),
})

function OperationsPage() {
  return (
    <div className="space-y-6">
      <section>
        <Badge>PHC and CHC monitoring</Badge>
        <h1 className="mt-3 text-3xl font-semibold tracking-tight">
          Operations
        </h1>
        <p className="mt-2 max-w-2xl text-muted-foreground">
          A compact view of hospital readiness, bed occupancy, doctor coverage,
          and the operational modules feeding the district command center.
        </p>
      </section>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {modules.map((module) => {
          const Icon = module.icon
          return (
            <Card key={module.label}>
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-base">
                  <Icon className="h-4 w-4 text-primary" />
                  {module.label}
                </CardTitle>
              </CardHeader>
              <CardContent className="text-sm text-muted-foreground">
                {module.value}
              </CardContent>
            </Card>
          )
        })}
      </section>

      <Card>
        <CardHeader>
          <CardTitle>Hospital Readiness</CardTitle>
          <CardDescription>
            Readiness combines inventory, beds, staffing, lab capacity, and load
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          {hospitals.map((hospital) => (
            <div key={hospital.name} className="rounded-lg border p-4">
              <div className="grid gap-4 md:grid-cols-[1fr_0.8fr_0.8fr_0.8fr] md:items-center">
                <div>
                  <div className="flex items-center gap-2">
                    <p className="font-medium">{hospital.name}</p>
                    <StatusBadge value={hospital.status} />
                  </div>
                  <p className="text-sm text-muted-foreground">
                    {hospital.type}
                  </p>
                </div>
                <p className="text-sm">Bed occupancy: {hospital.occupancy}%</p>
                <p className="text-sm">Doctors: {hospital.doctors}</p>
                <div>
                  <p className="mb-2 text-sm font-medium">
                    {hospital.readiness}/100
                  </p>
                  <ScoreBar value={hospital.readiness} />
                </div>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  )
}
