import { AppLayout } from "./components/layout/AppLayout";
import { IntegrationsPanel } from "./components/integrations/IntegrationsPanel";
import { ModelRoutingPanel } from "./components/config/ModelRoutingPanel";
import { ApprovalWorkflowPanel } from "./components/approvals/ApprovalWorkflowPanel";
import { SecurityPanel } from "./components/security/SecurityPanel";

export function AppShell() {
  return (
    <AppLayout>
      <ModelRoutingPanel />
      <IntegrationsPanel />
      <ApprovalWorkflowPanel />
      <SecurityPanel />
    </AppLayout>
  );
}
