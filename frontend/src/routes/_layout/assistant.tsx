import { createFileRoute } from "@tanstack/react-router"
import { Bot, SendHorizontal, Sparkles } from "lucide-react"

import { recommendations } from "@/components/HealSync/data"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"

export const Route = createFileRoute("/_layout/assistant")({
  component: AssistantPage,
  head: () => ({
    meta: [{ title: "AI Assistant | SwaasthSarvagya AI" }],
  }),
})

const prompts = [
  "Which hospitals require intervention today?",
  "Which medicines will run out this week?",
  "Why is PHC-12 marked critical?",
  "Show dengue affected hospitals.",
]

function AssistantPage() {
  return (
    <div className="space-y-6">
      <section>
        <Badge>Gemini-powered assistant</Badge>
        <h1 className="mt-3 text-3xl font-semibold tracking-tight">
          AI Assistant
        </h1>
        <p className="mt-2 max-w-2xl text-muted-foreground">
          Ask plain-language questions about hospitals, inventory, staffing,
          disease trends, and recommendations.
        </p>
      </section>

      <section className="grid gap-6 xl:grid-cols-[1fr_0.75fr]">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Bot className="h-4 w-4 text-primary" />
              District Query
            </CardTitle>
            <CardDescription>
              Static preview of the assistant experience
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="rounded-lg border bg-muted/40 p-4">
              <p className="text-sm text-muted-foreground">
                Which hospitals require intervention today?
              </p>
            </div>
            <div className="rounded-lg border p-4">
              <div className="mb-2 flex items-center gap-2">
                <Sparkles className="h-4 w-4 text-primary" />
                <p className="font-medium">HealSync summary</p>
              </div>
              <p className="text-sm text-muted-foreground">
                PHC-12 needs immediate medicine redistribution, CHC-4 needs
                evening staffing support, and District Hospital lab maintenance
                should be scheduled before tomorrow's projected demand peak.
              </p>
            </div>
            <div className="flex gap-2">
              <Input placeholder="Ask about stock-outs, beds, doctors, or outbreaks" />
              <Button aria-label="Send assistant query">
                <SendHorizontal className="h-4 w-4" />
              </Button>
            </div>
          </CardContent>
        </Card>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Suggested Prompts</CardTitle>
              <CardDescription>
                Common questions for district administrators
              </CardDescription>
            </CardHeader>
            <CardContent className="flex flex-wrap gap-2">
              {prompts.map((prompt) => (
                <Button key={prompt} variant="outline" size="sm">
                  {prompt}
                </Button>
              ))}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Explainable Recommendations</CardTitle>
              <CardDescription>
                Actions include source data and a human-readable reason
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              {recommendations.slice(0, 2).map((recommendation) => (
                <div
                  key={recommendation.action}
                  className="rounded-lg border p-3"
                >
                  <p className="font-medium">{recommendation.action}</p>
                  <p className="mt-1 text-sm text-muted-foreground">
                    {recommendation.reason}
                  </p>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>
      </section>
    </div>
  )
}
