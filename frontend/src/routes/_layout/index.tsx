import { createFileRoute } from "@tanstack/react-router"
import { Activity, AlertTriangle, Bot, TrendingUp } from "lucide-react"

import {
  alerts,
  hospitals,
  inventory,
  metrics,
  recommendations,
} from "@/components/HealSync/data"
import { ScoreBar, StatusBadge } from "@/components/HealSync/status"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import useAuth from "@/hooks/useAuth"

export const Route = createFileRoute("/_layout/")({
  component: Dashboard,
  head: () => ({
    meta: [
      {
        title: "HealSync AI Dashboard",
      },
    ],
  }),
})

function Dashboard() {
  const { user: currentUser } = useAuth()

  return (
    <div className="space-y-6">
      <section className="rounded-lg border bg-card p-6 shadow-sm">
        <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
          <div className="max-w-3xl space-y-3">
            <Badge className="w-fit">District health command center</Badge>
            <div>
              <h1 className="text-3xl font-semibold tracking-tight">
                HealSync AI
              </h1>
              <p className="mt-2 max-w-2xl text-muted-foreground">
                Welcome,{" "}
                {currentUser?.full_name || currentUser?.email || "operator"}.
                Monitor PHCs and CHCs, forecast shortages, and act on
                explainable AI recommendations before service gaps appear.
              </p>
            </div>
          </div>
          <Button asChild>
            <a href="/assistant">
              <Bot className="mr-2 h-4 w-4" />
              Ask AI Assistant
            </a>
          </Button>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {metrics.map((metric) => {
          const Icon = metric.icon
          return (
            <Card key={metric.title}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">
                  {metric.title}
                </CardTitle>
                <Icon className="h-4 w-4 text-primary" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-semibold">{metric.value}</div>
                <p className="mt-1 text-sm text-muted-foreground">
                  {metric.change}
                </p>
              </CardContent>
            </Card>
          )
        })}
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between gap-4">
              <div>
                <CardTitle>Operational Readiness</CardTitle>
                <CardDescription>
                  Live district snapshot across hospitals
                </CardDescription>
              </div>
              <Badge variant="secondary">
                <TrendingUp className="h-3.5 w-3.5" />
                Improving
              </Badge>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            {hospitals.slice(0, 3).map((hospital) => (
              <div key={hospital.name} className="rounded-lg border p-4">
                <div className="flex items-start justify-between gap-4">
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-2">
                      <p className="font-medium">{hospital.name}</p>
                      <StatusBadge value={hospital.status} />
                    </div>
                    <p className="mt-1 text-sm text-muted-foreground">
                      {hospital.patients} patients today, doctors{" "}
                      {hospital.doctors}
                    </p>
                  </div>
                  <div className="w-32 text-right">
                    <p className="text-sm font-medium">
                      {hospital.readiness}/100
                    </p>
                    <ScoreBar value={hospital.readiness} />
                  </div>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="h-4 w-4 text-amber-500" />
              Priority Alerts
            </CardTitle>
            <CardDescription>
              AI-generated interventions that need attention
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {alerts.slice(0, 3).map((alert) => (
              <div key={alert.title} className="rounded-lg border p-4">
                <div className="mb-2 flex items-center justify-between gap-2">
                  <p className="font-medium">{alert.title}</p>
                  <StatusBadge value={alert.severity} />
                </div>
                <p className="text-sm text-muted-foreground">{alert.detail}</p>
              </div>
            ))}
          </CardContent>
        </Card>
      </section>

      <section className="grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
        <Card>
          <CardHeader>
            <CardTitle>Inventory Watchlist</CardTitle>
            <CardDescription>Critical medicines and lab items</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {inventory.slice(0, 3).map((item) => (
              <div
                key={item.item}
                className="flex items-center justify-between gap-4 rounded-lg border p-3"
              >
                <div>
                  <p className="font-medium">{item.item}</p>
                  <p className="text-sm text-muted-foreground">
                    {item.hospital} has {item.stock} units
                  </p>
                </div>
                <StatusBadge value={item.risk} />
              </div>
            ))}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Bot className="h-4 w-4" />
              Recommended Actions
            </CardTitle>
            <CardDescription>
              Explainable next steps for district administrators
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {recommendations.slice(0, 2).map((recommendation) => {
              const Icon = recommendation.icon
              return (
                <div
                  key={recommendation.action}
                  className="rounded-lg border p-4"
                >
                  <div className="flex gap-3">
                    <Icon className="mt-1 h-4 w-4 text-primary" />
                    <div>
                      <p className="font-medium">{recommendation.action}</p>
                      <p className="mt-1 text-sm text-muted-foreground">
                        {recommendation.reason}
                      </p>
                    </div>
                  </div>
                </div>
              )
            })}
            <div className="flex items-center justify-between rounded-lg border border-primary/20 bg-primary/10 p-3">
              <div>
                <p className="font-medium">Gemini summary ready</p>
                <p className="text-sm text-muted-foreground">
                  Actionable explanation and next steps included.
                </p>
              </div>
              <Activity className="h-5 w-5 text-primary" />
            </div>
          </CardContent>
        </Card>
      </section>
    </div>
  )
}
