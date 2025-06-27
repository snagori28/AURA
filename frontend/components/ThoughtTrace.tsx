interface StepProps {
  step: string;
}

export default function ThoughtTrace({ step }: StepProps) {
  return (
    <div className="p-2 bg-gray-800 rounded mb-2 text-sm">
      {step}
    </div>
  );
}
