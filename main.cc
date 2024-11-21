#define NS3_LOG_ENABLE 1
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/lte-module.h"
#include "ns3/mobility-module.h"
#include "ns3/config-store.h"

using namespace ns3;


int main(int argc, char *argv[]) {

  NodeContainer enbNodes;
  enbNodes.Create(1);

  NodeContainer ueNodes;
  enbNodes.Create(2);

  // LTE module creation

  Ptr<LteHelper> lteHelper = CreateObject<LteHelper>();

  // Mobility module creation

  MobilityHelper mobility;
  mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel");
  mobility.Install(enbNodes);
  mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel");
  mobility.Install(ueNodes);

  // Network configuration

  NetDeviceContainer enbDevs = lteHelper->InstallEnbDevice(enbNodes);
  NetDeviceContainer ueDevs = lteHelper->InstallUeDevice(ueNodes);

  // attaching UEs to eNB && activating a data radio bareer
  
  lteHelper->Attach(ueDevs, enbDevs.Get(0));
  enum EpsBearer::Qci q = EpsBearer::GBR_CONV_VOICE;
  EpsBearer bearer(q);
  lteHelper->ActivateDataRadioBearer(ueDevs, bearer);

  // pfffmacscheduler

  lteHelper->SetSchedulerType("ns3::PfFfMacScheduler");


  // RLC & MAC characteristics output

  lteHelper->EnableRlcTraces();
  lteHelper->EnableMacTraces();



  // simulation
  Simulator::Stop(Seconds(0.005));
  Simulator::Run();
  Simulator::Destroy();

  return 0;
}
