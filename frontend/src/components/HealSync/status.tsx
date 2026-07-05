import { Badge } from "@/components/ui/badge"

type StatusBadgeProps = {
  value: string
}

export function StatusBadge({ value }: StatusBadgeProps) {
  if (["High", "Critical"].includes(value)) {
    return <Badge variant="destructive">{value}</Badge>
  }

  if (["Medium", "Watch"].includes(value)) {
    return <Badge variant="secondary">{value}</Badge>
  }

  return <Badge variant="outline">{value}</Badge>
}

type ScoreBarProps = {
  value: number
}

export function ScoreBar({ value }: ScoreBarProps) {
  return (
    <div className="h-2 w-full overflow-hidden rounded-full bg-muted">
      <div
        className="h-full rounded-full bg-primary"
        style={{ width: `${value}%` }}
      />
    </div>
  )
}
