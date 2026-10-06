"""Banco del AWS Certified Solutions Architect – Associate (SAA-C03).

Escrito a mano y revisado contra la documentación de AWS (octubre 2026).
Genera datos/aws_a.json con el esquema de ESQUEMA.md; la respuesta correcta se
coloca en una posición barajada con semilla fija para que el archivo sea estable.
"""
import json
import os
import random

TASK = {"secure": "Diseño seguro", "resilient": "Diseño resiliente",
        "performance": "Alto rendimiento", "cost": "Optimización de costes"}

Q = []


def q(sec, lvl, text, right, wrong, e):
    """right: str (una correcta) o lista (respuesta múltiple)."""
    Q.append((sec, lvl, text, right, wrong, e))


# ---------------- Diseño seguro (30 %) ----------------
S = "secure"
q(S, 1, "An application running on Amazon EC2 needs to read objects from an Amazon S3 bucket. What is the MOST secure way to give the application access?",
  "Attach an IAM role with the required S3 permissions to the EC2 instance",
  ["Store an IAM user's access keys in the application code", "Save the root user's access keys in environment variables", "Make the S3 bucket public and restrict it by file name"],
  "EC2 + acceso a otro servicio = ROL de IAM (instance profile). Nunca claves guardadas en código ni la cuenta root.")
q(S, 1, "A company wants to follow AWS best practices for the root user of its account. What should it do?",
  "Enable MFA on the root user and use other identities for daily tasks",
  ["Share the root password with all administrators", "Create access keys for the root user for automation", "Use the root user only through the AWS CLI"],
  "Root: MFA activado y guardado en un cajón. Para el día a día, usuarios o IAM Identity Center.")
q(S, 2, "A company must encrypt S3 objects at rest. It must control the key, rotate it automatically and audit every use of the key in AWS CloudTrail. Which option meets these requirements?",
  "Server-side encryption with AWS KMS customer managed keys (SSE-KMS)",
  ["Server-side encryption with Amazon S3 managed keys (SSE-S3)", "Server-side encryption with customer-provided keys (SSE-C)", "Store the objects in S3 Glacier"],
  "«Auditar el uso de la clave» + «controlar la clave» = KMS con clave gestionada por el cliente. SSE-S3 no deja controlarla ni auditarla.")
q(S, 1, "An application needs to store database credentials securely and rotate them automatically every 30 days. Which service should be used?",
  "AWS Secrets Manager",
  ["AWS Systems Manager Parameter Store standard parameters", "An encrypted file in Amazon S3", "Environment variables in AWS Lambda"],
  "Palabra clave «rotación automática de credenciales» = Secrets Manager. Parameter Store no rota por sí solo.")
q(S, 1, "EC2 instances in a private subnet must download software updates from the internet. The instances must not be reachable from the internet. What should a solutions architect do?",
  "Create a NAT gateway in a public subnet and add a route to it from the private subnet",
  ["Attach an internet gateway to the private subnet route table", "Assign Elastic IP addresses to the instances", "Create a gateway VPC endpoint for the internet"],
  "Salida a internet desde subred privada sin entrada = NAT gateway (en subred PÚBLICA).")
q(S, 2, "EC2 instances in a private subnet need to access Amazon S3. Traffic must not go over the internet and the company wants to avoid NAT gateway data processing charges. What is the solution?",
  "Create a gateway VPC endpoint for Amazon S3 and update the route table",
  ["Create a NAT gateway in each Availability Zone", "Use an internet gateway with a security group", "Create a VPN connection to Amazon S3"],
  "S3 o DynamoDB desde subred privada = gateway endpoint: gratis y sin internet.")
q(S, 1, "A web application behind an Application Load Balancer is receiving SQL injection and cross-site scripting attacks. Which service protects it?",
  "AWS WAF",
  ["AWS Shield Standard", "Amazon GuardDuty", "Network ACLs"],
  "Ataques de capa 7 (SQL injection, XSS, filtrar por IP o país) = WAF.")
q(S, 2, "A company needs protection against large DDoS attacks, access to a 24/7 AWS response team and protection against scaling charges caused by attacks. Which service should it use?",
  "AWS Shield Advanced",
  ["AWS Shield Standard", "AWS WAF only", "Amazon Inspector"],
  "DDoS + equipo de respuesta 24/7 + protección de costes = Shield ADVANCED. Standard es gratis y básico.")
q(S, 1, "A company must find and classify personally identifiable information (PII) stored in Amazon S3 buckets. Which service should it use?",
  "Amazon Macie",
  ["Amazon GuardDuty", "Amazon Inspector", "AWS Config"],
  "Datos personales (PII) en S3 = Macie.")
q(S, 1, "Which service continuously analyzes CloudTrail events, VPC Flow Logs and DNS logs to detect malicious activity?",
  "Amazon GuardDuty",
  ["Amazon Macie", "AWS Trusted Advisor", "AWS Artifact"],
  "Detección de amenazas analizando logs = GuardDuty.")
q(S, 1, "A company wants automated vulnerability scanning of its EC2 instances and container images in Amazon ECR. Which service meets this need?",
  "Amazon Inspector",
  ["Amazon Macie", "AWS Shield", "Amazon Detective"],
  "Vulnerabilidades de software (CVE) en EC2, ECR y Lambda = Inspector.")
q(S, 1, "An auditor needs a record of every API call made in the company's AWS account, including who made it and when. Which service provides this?",
  "AWS CloudTrail",
  ["Amazon CloudWatch metrics", "AWS Config", "VPC Flow Logs"],
  "¿Quién hizo qué y cuándo? = CloudTrail. CloudWatch = métricas y logs de rendimiento.")
q(S, 2, "A company uses AWS Organizations. It must prevent all member accounts from leaving the organization or disabling AWS CloudTrail, even administrators. What should it use?",
  "A service control policy (SCP) attached to the organizational units",
  ["IAM policies in each account", "AWS Config rules", "S3 bucket policies"],
  "Restringir a TODA una cuenta, incluido su admin = SCP de Organizations. Las SCP no conceden permisos, solo limitan.")
q(S, 2, "Static content in an S3 bucket is served through Amazon CloudFront. Users must not be able to access the bucket directly. What should be configured?",
  "Origin access control (OAC) on CloudFront and a bucket policy that allows only CloudFront",
  ["Make the bucket public and use signed cookies", "Enable S3 Transfer Acceleration", "Use a NAT gateway in front of the bucket"],
  "S3 accesible solo por CloudFront = OAC (sustituye a la antigua OAI).")
q(S, 1, "A company must share a private S3 object with an external partner who has no AWS account. Access must expire after 24 hours. What is the simplest solution?",
  "Generate an S3 presigned URL that expires in 24 hours",
  ["Create an IAM user for the partner", "Make the object public for one day", "Copy the object to a public bucket"],
  "Acceso temporal a un objeto sin cuenta AWS = URL prefirmada.")
q(S, 2, "A security team must block traffic from one specific malicious IP address to all instances in a subnet. What should they use?",
  "A deny rule in the subnet's network ACL",
  ["A deny rule in the security group", "An IAM policy", "A Route 53 health check"],
  "Los security groups solo PERMITEN; para DENEGAR una IP, network ACL.")
q(S, 2, "Which statement about security groups and network ACLs is correct?",
  "Security groups are stateful; network ACLs are stateless and need rules for return traffic",
  ["Security groups are stateless; network ACLs are stateful", "Both are stateful and support deny rules", "Network ACLs are applied to individual instances"],
  "SG = con estado, a nivel de instancia, solo allow. NACL = sin estado, a nivel de subred, allow y deny, reglas numeradas.")
q(S, 2, "A company with many AWS accounts wants employees to sign in once with their corporate identity provider and access the accounts they are assigned to. What should it use?",
  "AWS IAM Identity Center",
  ["An IAM user in every account for each employee", "Amazon Cognito user pools", "Shared root credentials"],
  "Empleados + varias cuentas + inicio de sesión único = IAM Identity Center (antes AWS SSO).")
q(S, 1, "A mobile app needs user sign-up and sign-in, including sign-in with Google and Facebook. Which service should be used?",
  "Amazon Cognito user pools",
  ["IAM users", "AWS IAM Identity Center", "AWS Directory Service"],
  "Usuarios de una APP (clientes, redes sociales) = Cognito. Empleados = Identity Center.")
q(S, 2, "A company requires that all new Amazon EBS volumes in a Region are encrypted automatically. What is the simplest solution?",
  "Enable EBS encryption by default for the Region",
  ["Write a Lambda function that encrypts volumes after creation", "Use AWS Config to delete unencrypted volumes", "Encrypt each volume manually"],
  "«Por defecto» + «simplest» = la opción de cifrado de EBS por defecto en la región.")
q(S, 3, "Financial records in Amazon S3 must not be deleted or overwritten by anyone, including the root user, for 7 years. What should be configured?",
  "S3 Object Lock in compliance mode with a 7-year retention period",
  ["S3 Object Lock in governance mode", "S3 Versioning with lifecycle rules", "An IAM policy that denies s3:DeleteObject"],
  "«Nadie, ni root» = Object Lock en modo COMPLIANCE. En governance, usuarios con permiso especial sí pueden.")
q(S, 2, "A company wants to protect important S3 objects against accidental deletion and be able to recover previous versions. What should it enable?",
  "S3 Versioning (optionally with MFA Delete)",
  ["S3 Transfer Acceleration", "S3 Standard-IA", "Server access logging"],
  "Recuperar versiones y borrados accidentales = Versioning. MFA Delete añade una segunda llave para borrar.")
q(S, 1, "An Application Load Balancer must serve HTTPS with a free certificate that renews automatically. Which service provides the certificate?",
  "AWS Certificate Manager (ACM)",
  ["AWS KMS", "AWS CloudHSM", "AWS Secrets Manager"],
  "Certificados TLS gratis y renovación automática para ALB/CloudFront = ACM.")
q(S, 3, "Regulations require that encryption keys are stored in dedicated, single-tenant hardware security modules fully controlled by the company. Which service meets this requirement?",
  "AWS CloudHSM",
  ["AWS KMS with AWS managed keys", "SSE-S3", "AWS Secrets Manager"],
  "HSM dedicado de un solo cliente, control total = CloudHSM.")
q(S, 2, "A web application has an ALB in public subnets and EC2 instances in private subnets. Which TWO actions improve security? (Choose TWO.)",
  ["Allow inbound traffic to the instances only from the ALB's security group", "Keep the EC2 instances in private subnets without public IP addresses"],
  ["Allow SSH (port 22) from 0.0.0.0/0", "Assign public IP addresses to the instances", "Allow all traffic in the network ACLs"],
  "Patrón clásico: ALB público, EC2 privadas, y el SG de las EC2 solo acepta el SG del ALB.")
q(S, 2, "A company must detect S3 buckets that become public and automatically fix them. Which service can evaluate resource configurations and trigger remediation?",
  "AWS Config with managed rules and automatic remediation",
  ["AWS CloudTrail Insights", "Amazon Inspector", "AWS Trusted Advisor only"],
  "Cumplimiento de configuración + remediación = AWS Config.")
q(S, 2, "A security team wants one dashboard that aggregates findings from GuardDuty, Inspector and Macie across accounts. What should it use?",
  "AWS Security Hub",
  ["Amazon Detective", "AWS Artifact", "Amazon CloudWatch dashboards"],
  "Vista central de hallazgos de seguridad = Security Hub.")
q(S, 1, "A Lambda function must write items to a DynamoDB table. How should permissions be granted?",
  "Give the function an execution role with a policy that allows the required DynamoDB actions",
  ["Store an access key in the function code", "Make the table public", "Use the root account credentials"],
  "Lambda accede a otros servicios mediante su ROL de ejecución.")
q(S, 3, "A company wants to expose an internal service in its VPC to hundreds of customer VPCs in other accounts. Traffic must stay private and CIDR ranges may overlap. Which solution should be used?",
  "AWS PrivateLink with a Network Load Balancer and a VPC endpoint service",
  ["VPC peering with each customer", "A transit gateway shared with all customers", "A public ALB with security groups"],
  "Exponer UN servicio a muchas VPC, privado y con CIDR solapados = PrivateLink. El peering no admite solapamiento.")
q(S, 1, "A company wants to make sure no S3 bucket in the account can ever be made public by mistake. What should it enable?",
  "S3 Block Public Access at the account level",
  ["S3 Versioning", "Default encryption", "S3 Intelligent-Tiering"],
  "Evitar buckets públicos en toda la cuenta = Block Public Access a nivel de cuenta.")
q(S, 2, "Administrators need shell access to EC2 instances in private subnets without opening inbound ports or managing bastion hosts. What should they use?",
  "AWS Systems Manager Session Manager",
  ["A bastion host with port 22 open", "EC2 Instance Connect with a public IP", "A NAT gateway"],
  "Acceso a instancias sin puertos ni bastión y con registro = Session Manager.")
q(S, 2, "Which TWO practices follow the principle of least privilege? (Choose TWO.)",
  ["Grant only the permissions required for each task", "Use IAM roles with temporary credentials instead of long-term access keys"],
  ["Attach the AdministratorAccess policy to every developer", "Share one IAM user among the team", "Create access keys for the root user"],
  "Mínimo privilegio = solo lo necesario + credenciales temporales (roles).")
q(S, 2, "A company stores data in S3 that must be accessed by another AWS account. What is the recommended way to grant access?",
  "Add a bucket policy that grants access to a role in the other account",
  ["Make the bucket public", "Share the access keys of an IAM user", "Copy the data into the other account every night"],
  "Acceso entre cuentas a S3 = bucket policy que confía en un rol/cuenta externa.")
q(S, 3, "An API in Amazon API Gateway must only accept requests from users who signed in through an Amazon Cognito user pool. What should be configured?",
  "A Cognito user pool authorizer on the API Gateway methods",
  ["An IAM user for each customer", "A NAT gateway", "AWS WAF geo match rules"],
  "API Gateway + usuarios de Cognito = autorizador de Cognito (valida el token JWT).")

# ---------------- Diseño resiliente (26 %) ----------------
R = "resilient"
q(R, 1, "A web application runs on a single EC2 instance. How can a solutions architect make it highly available?",
  "Use an Auto Scaling group across multiple Availability Zones behind an Application Load Balancer",
  ["Use a larger instance type", "Take daily EBS snapshots", "Move the instance to a dedicated host"],
  "Alta disponibilidad = varias AZ + Auto Scaling + balanceador. Más grande no es más disponible.")
q(R, 1, "A company needs its Amazon RDS for MySQL database to fail over automatically if the primary Availability Zone fails. What should it use?",
  "RDS Multi-AZ deployment",
  ["A read replica in the same AZ", "Daily manual snapshots", "A larger DB instance class"],
  "Failover AUTOMÁTICO = Multi-AZ. Las read replicas son para escalar LECTURAS.")
q(R, 1, "An RDS database is overloaded by reporting queries that only read data. How can the load be reduced?",
  "Create read replicas and send the reporting queries to them",
  ["Enable Multi-AZ", "Increase the backup retention period", "Use S3 Glacier for the database"],
  "Escalar lecturas = read replicas. Multi-AZ NO sirve para leer en la mayoría de motores.")
q(R, 1, "An order system must handle sudden traffic spikes without losing orders. The processing tier sometimes cannot keep up. What should be added between the tiers?",
  "An Amazon SQS queue",
  ["An Amazon SNS topic only", "A larger EC2 instance", "A NAT gateway"],
  "Desacoplar y amortiguar picos sin perder mensajes = SQS.")
q(R, 2, "Messages about financial transactions must be processed exactly once and in the order they were sent. Which service should be used?",
  "Amazon SQS FIFO queue",
  ["Amazon SQS standard queue", "Amazon SNS standard topic", "Amazon Kinesis Data Firehose"],
  "Orden + exactamente una vez = SQS FIFO. La estándar puede duplicar y desordenar.")
q(R, 2, "When a new order is placed, three independent services (billing, shipping, analytics) must each receive a copy of the message. What is the best design?",
  "Publish to an SNS topic with an SQS queue subscribed for each service (fan-out)",
  ["Use one SQS queue shared by the three services", "Write the message to S3 and poll it", "Call each service directly from the web tier"],
  "Una noticia a varios destinos = SNS + SQS (fan-out).")
q(R, 2, "A company needs a disaster recovery plan with the LOWEST cost. An RTO of 24 hours is acceptable. Which strategy should it use?",
  "Backup and restore",
  ["Pilot light", "Warm standby", "Multi-site active-active"],
  "DR de más barato a más rápido: backup&restore → pilot light → warm standby → multi-site. RTO de horas = backup&restore.")
q(R, 3, "A company needs DR in another Region with an RTO of a few minutes. A scaled-down but fully working copy of the production environment must always run there. Which strategy is this?",
  "Warm standby",
  ["Backup and restore", "Pilot light", "Cold standby"],
  "Copia reducida PERO funcionando = warm standby. Pilot light solo mantiene lo esencial (datos) encendido.")
q(R, 3, "A global application uses Amazon Aurora MySQL. It needs a cross-Region DR solution with an RPO of about 1 second and an RTO of less than 1 minute. What should be used?",
  "Amazon Aurora Global Database",
  ["Aurora Multi-AZ in one Region", "Daily snapshots copied to another Region", "AWS DMS replication"],
  "Aurora + otra región + RPO de 1 s = Aurora Global Database.")
q(R, 2, "A DynamoDB-based application must be active in two Regions, with users writing in either Region. Which feature should be used?",
  "DynamoDB global tables",
  ["DynamoDB Accelerator (DAX)", "DynamoDB Streams with Lambda in one Region", "On-demand backups"],
  "DynamoDB multirregión activo-activo = global tables.")
q(R, 1, "A company must automatically copy new objects from an S3 bucket in us-east-1 to a bucket in eu-west-1. What should it configure?",
  "S3 Cross-Region Replication (with versioning enabled on both buckets)",
  ["S3 Transfer Acceleration", "S3 lifecycle rules", "A CloudFront distribution"],
  "Copiar objetos a otra región = CRR. Requiere versionado en ambos buckets.")
q(R, 2, "If the primary Region becomes unhealthy, users must automatically be sent to a standby site in another Region. Which Route 53 feature should be used?",
  "Failover routing with health checks",
  ["Simple routing", "Weighted routing without health checks", "Geolocation routing"],
  "Pasar al sitio de respaldo cuando cae el principal = failover routing + health checks.")
q(R, 1, "Many Linux EC2 instances in several Availability Zones need to share the same files at the same time. Which storage should be used?",
  "Amazon EFS",
  ["Amazon EBS gp3 volume", "Instance store", "Amazon S3 Glacier"],
  "Sistema de archivos compartido Linux (NFS) multi-AZ = EFS. EBS se conecta normalmente a una sola instancia.")
q(R, 2, "Windows applications need a shared file system that uses SMB and integrates with Active Directory. Which service fits best?",
  "Amazon FSx for Windows File Server",
  ["Amazon EFS", "Amazon FSx for Lustre", "Amazon S3"],
  "Windows + SMB + Active Directory = FSx for Windows.")
q(R, 2, "A workflow must run several Lambda functions in order, with retries, error handling and a wait for human approval. What should be used?",
  "AWS Step Functions",
  ["Amazon SQS", "Amazon EventBridge Scheduler", "One very large Lambda function"],
  "Orquestar pasos con reintentos y esperas = Step Functions.")
q(R, 2, "Some messages in an SQS queue fail processing repeatedly and block other work. How should they be handled?",
  "Configure a dead-letter queue with a maximum receive count",
  ["Delete the queue", "Increase the message size limit", "Switch to an SNS topic"],
  "Mensajes que fallan una y otra vez = dead-letter queue.")
q(R, 1, "A company wants a central service to schedule and manage backups for EBS, RDS, DynamoDB and EFS with retention policies. Which service should it use?",
  "AWS Backup",
  ["AWS DataSync", "Amazon S3 Glacier", "AWS Storage Gateway"],
  "Copias de seguridad centralizadas con políticas = AWS Backup.")
q(R, 2, "Users are logged out whenever the Auto Scaling group terminates an instance because sessions are stored in instance memory. How should this be fixed?",
  "Store session data in Amazon ElastiCache or DynamoDB",
  ["Disable scale-in", "Use larger instances", "Enable sticky sessions only"],
  "Aplicación sin estado: las sesiones fuera de la instancia (ElastiCache o DynamoDB).")
q(R, 2, "Instances in an Auto Scaling group keep running even when the application returns errors, because EC2 status checks still pass. What should be changed?",
  "Enable Elastic Load Balancing health checks for the Auto Scaling group",
  ["Increase the instance size", "Disable health checks", "Add a NAT gateway"],
  "Que ASG sustituya instancias con la app rota = health checks del ELB.")
q(R, 1, "Traffic always increases every Monday at 9:00 a.m. How should the Auto Scaling group prepare?",
  "Create a scheduled scaling action before 9:00 a.m. on Mondays",
  ["Use only manual scaling", "Use a larger instance all week", "Disable Auto Scaling"],
  "Pico predecible = scheduled scaling.")
q(R, 2, "A company wants its Auto Scaling group to keep average CPU utilization at about 50%. Which policy is simplest?",
  "Target tracking scaling policy",
  ["Step scaling with many alarms", "Scheduled scaling", "Manual scaling"],
  "Mantener una métrica en un valor = target tracking.")
q(R, 2, "A company needs to migrate an on-premises Oracle database to Amazon RDS with minimal downtime. What should it use?",
  "AWS Database Migration Service (DMS) with ongoing replication",
  ["AWS DataSync", "AWS Snowball Edge", "Manual export to S3 and import"],
  "Migrar bases de datos con poco corte = DMS (+ SCT si cambia el motor).")
q(R, 2, "A company must move 500 TB of data from its data center to Amazon S3. Its internet connection is slow. What is the fastest option?",
  "AWS Snowball Edge devices",
  ["AWS Site-to-Site VPN", "S3 Transfer Acceleration", "Uploading with the AWS CLI"],
  "Cientos de TB con poco ancho de banda = Snowball (dispositivo físico).")
q(R, 2, "A company wants to automatically and securely copy data online from an on-premises NFS server to Amazon EFS on a schedule. Which service should be used?",
  "AWS DataSync",
  ["AWS Snowball Edge", "AWS Database Migration Service", "Amazon Data Firehose"],
  "Transferencia de archivos ONLINE programada = DataSync.")
q(R, 2, "On-premises applications must store files in Amazon S3 through an NFS share, with a local cache for frequently used files. What should be deployed?",
  "AWS Storage Gateway – S3 File Gateway",
  ["AWS DataSync", "Amazon EFS", "AWS Direct Connect only"],
  "On-premises + NFS/SMB + guarda en S3 + caché local = File Gateway.")
q(R, 3, "A global gaming application uses TCP and UDP. It needs two static IP addresses and fast automatic failover between Regions. Which service should be used?",
  "AWS Global Accelerator",
  ["Amazon CloudFront", "Route 53 simple routing", "An Application Load Balancer"],
  "IP estáticas + TCP/UDP + failover entre regiones = Global Accelerator. CloudFront es para contenido HTTP cacheable.")
q(R, 2, "A company has 30 VPCs and an on-premises network. It wants a hub-and-spoke design instead of many peering connections. What should it use?",
  "AWS Transit Gateway",
  ["VPC peering between all VPCs", "A NAT gateway", "An internet gateway"],
  "Muchas VPC + on-prem en estrella = Transit Gateway.")
q(R, 3, "A company has an AWS Direct Connect link and needs a low-cost, encrypted backup connection in case it fails. What should it add?",
  "An AWS Site-to-Site VPN connection",
  ["A second internet gateway", "VPC peering", "Amazon CloudFront"],
  "Respaldo barato y cifrado de Direct Connect = Site-to-Site VPN.")
q(R, 2, "Which TWO changes make an application that runs on one EC2 instance more resilient? (Choose TWO.)",
  ["Run instances in an Auto Scaling group across multiple Availability Zones", "Place an Application Load Balancer in front of the instances"],
  ["Use a bigger instance type", "Keep all instances in one Availability Zone", "Store data on instance store volumes"],
  "Resiliencia = multi-AZ + autoescalado + balanceador.")
q(R, 2, "Clickstream data must be ingested in real time, kept for several days and read by multiple applications that may need to replay it. Which service fits best?",
  "Amazon Kinesis Data Streams",
  ["Amazon SQS standard queue", "Amazon SNS", "AWS Batch"],
  "Tiempo real + varios consumidores + volver a leer = Kinesis Data Streams.")
q(R, 1, "A company needs to restore an RDS database to any second within the last 7 days. What should be enabled?",
  "Automated backups with a 7-day retention period",
  ["Read replicas", "Multi-AZ only", "Enhanced monitoring"],
  "Point-in-time recovery = backups automáticos (hasta 35 días).")
q(R, 2, "To prepare for a regional disaster, a company wants copies of its EBS data in another Region. What is the simplest approach?",
  "Copy EBS snapshots to the other Region (for example with AWS Backup)",
  ["Attach the volume to an instance in the other Region", "Use RAID 1 across Regions", "Enable Multi-AZ on the volume"],
  "EBS vive en una AZ; para otra región, copia los snapshots.")

# ---------------- Alto rendimiento (24 %) ----------------
P = "performance"
q(P, 1, "A website has users around the world. Images and videos load slowly far from the origin Region. What should be used?",
  "Amazon CloudFront",
  ["A larger EC2 instance", "Amazon RDS read replicas", "AWS Direct Connect"],
  "Contenido estático para usuarios globales = CloudFront (CDN).")
q(P, 2, "A DynamoDB table receives many repeated reads and needs microsecond read latency with minimal code changes. What should be added?",
  "DynamoDB Accelerator (DAX)",
  ["Amazon ElastiCache for Redis with custom code", "RDS read replicas", "S3 Transfer Acceleration"],
  "DynamoDB + microsegundos = DAX.")
q(P, 1, "The same expensive queries run thousands of times per minute against an RDS database. How can performance be improved?",
  "Add an Amazon ElastiCache cluster to cache query results",
  ["Enable Multi-AZ", "Use S3 Glacier", "Add a NAT gateway"],
  "Consultas repetidas = caché en memoria (ElastiCache).")
q(P, 2, "Users on several continents upload large files to a single S3 bucket and uploads are slow. Which TWO features improve upload speed? (Choose TWO.)",
  ["S3 Transfer Acceleration", "Multipart upload"],
  ["S3 Glacier Deep Archive", "S3 Versioning", "S3 Object Lock"],
  "Subidas lejanas = Transfer Acceleration. Archivos grandes = multipart (recomendado > 100 MB).")
q(P, 2, "A database on EC2 needs the highest and most consistent IOPS from Amazon EBS. Which volume type should be chosen?",
  "Provisioned IOPS SSD (io2 Block Express)",
  ["Throughput Optimized HDD (st1)", "Cold HDD (sc1)", "General Purpose SSD (gp2) with burst"],
  "Bases de datos exigentes = io2/io1 (Provisioned IOPS).")
q(P, 2, "An application needs very fast temporary scratch storage. Losing the data when the instance stops is acceptable. Which storage gives the best performance?",
  "EC2 instance store",
  ["Amazon EFS", "Amazon S3", "EBS sc1"],
  "Temporal + máxima velocidad + se puede perder = instance store.")
q(P, 2, "A log-processing workload reads large files sequentially and needs high throughput at low cost on EBS. Which volume type fits best?",
  "Throughput Optimized HDD (st1)",
  ["Provisioned IOPS SSD (io2)", "Cold HDD (sc1)", "EC2 instance store"],
  "Mucho throughput secuencial y barato = st1. sc1 es para datos fríos poco usados.")
q(P, 1, "Which EBS volume type lets you set IOPS and throughput independently from the volume size at a low price?",
  "General Purpose SSD (gp3)",
  ["gp2", "st1", "Magnetic standard"],
  "gp3: IOPS y throughput independientes del tamaño; suele ser más barato que gp2.")
q(P, 2, "An HPC application needs the lowest possible network latency between EC2 instances. Which placement group should be used?",
  "Cluster placement group",
  ["Spread placement group", "Partition placement group", "No placement group"],
  "Latencia mínima entre instancias = cluster (mismas rack/AZ).")
q(P, 2, "A small number of critical instances must each run on distinct hardware to reduce the risk of simultaneous failure. Which placement group should be used?",
  "Spread placement group",
  ["Cluster placement group", "Partition placement group in one partition", "Dedicated Host"],
  "Cada instancia en hardware distinto = spread.")
q(P, 1, "Analysts want to run SQL queries directly on CSV and Parquet files in S3 without managing servers. Which service should they use?",
  "Amazon Athena",
  ["Amazon RDS", "Amazon DynamoDB", "Amazon ElastiCache"],
  "SQL sobre S3 sin servidores = Athena.")
q(P, 1, "A company needs a data warehouse to run complex analytic queries on petabytes of structured data. Which service fits best?",
  "Amazon Redshift",
  ["Amazon DynamoDB", "Amazon RDS for MySQL", "Amazon Neptune"],
  "Data warehouse / OLAP = Redshift.")
q(P, 2, "Streaming data must be delivered to Amazon S3 in near real time, without writing code to manage consumers. Which service should be used?",
  "Amazon Data Firehose",
  ["Amazon Kinesis Data Streams with custom consumers", "Amazon SQS", "AWS Batch"],
  "Entregar streaming a S3/Redshift sin código = Data Firehose (antes «Kinesis Data Firehose»). «Near real time» es su palabra clave.")
q(P, 1, "Every time an image is uploaded to S3, a thumbnail must be created. What is the most efficient design?",
  "Use an S3 event notification to invoke a Lambda function",
  ["Run an EC2 instance that checks the bucket every minute", "Use a cron job on premises", "Use S3 Glacier"],
  "Reaccionar a subidas a S3 = evento de S3 → Lambda.")
q(P, 2, "An application needs a NoSQL key-value database with single-digit millisecond latency at any scale and unpredictable traffic. What should be used?",
  "Amazon DynamoDB with on-demand capacity",
  ["Amazon RDS for PostgreSQL", "Amazon Redshift", "Amazon S3 Glacier"],
  "Clave-valor, cualquier escala, tráfico impredecible = DynamoDB on-demand.")
q(P, 2, "A relational application has intermittent and unpredictable workloads. The database must scale capacity automatically. What fits best?",
  "Amazon Aurora Serverless v2",
  ["RDS on a fixed large instance", "Amazon DynamoDB", "Amazon Redshift"],
  "Relacional + carga variable + autoescalado = Aurora Serverless v2.")
q(P, 1, "A team wants to run Docker containers without managing EC2 servers or clusters of instances. Which option fits best?",
  "Amazon ECS with AWS Fargate",
  ["Amazon ECS on self-managed EC2", "AWS Elastic Beanstalk on EC2", "Amazon Lightsail"],
  "Contenedores sin gestionar servidores = Fargate.")
q(P, 2, "A company already uses Kubernetes and wants a managed Kubernetes control plane on AWS. Which service should it use?",
  "Amazon EKS",
  ["Amazon ECS", "AWS App Runner", "AWS Batch"],
  "Kubernetes = EKS. ECS es el orquestador propio de AWS.")
q(P, 2, "Requests to /api must go to one target group and requests to /images to another, using one load balancer. Which load balancer should be used?",
  "Application Load Balancer with path-based routing rules",
  ["Network Load Balancer", "Gateway Load Balancer", "Classic Load Balancer"],
  "Enrutado por ruta o host (capa 7) = ALB.")
q(P, 2, "An application needs to handle millions of TCP requests per second with ultra-low latency and a static IP per Availability Zone. Which load balancer should be used?",
  "Network Load Balancer",
  ["Application Load Balancer", "Classic Load Balancer", "Gateway Load Balancer"],
  "TCP/UDP + rendimiento extremo + IP estática = NLB.")
q(P, 1, "A company wants to publish a REST API in front of Lambda functions, with throttling, API keys and response caching. Which service should be used?",
  "Amazon API Gateway",
  ["Amazon CloudFront only", "Network Load Balancer", "AWS AppSync"],
  "API REST + throttling + API keys = API Gateway.")
q(P, 3, "A latency-sensitive Lambda function suffers from cold starts during traffic peaks. What should be configured?",
  "Provisioned concurrency",
  ["Reserved concurrency set to 0", "A larger deployment package", "A dead-letter queue"],
  "Eliminar arranques en frío = provisioned concurrency.")
q(P, 2, "Users should be routed to the AWS Region that gives them the fastest response. Which Route 53 routing policy should be used?",
  "Latency-based routing",
  ["Geolocation routing", "Weighted routing", "Simple routing"],
  "«Más rápido» = latency. «Según el país» = geolocation.")
q(P, 2, "Because of licensing, content must be shown only to users in specific countries. Which TWO options can do this? (Choose TWO.)",
  ["CloudFront geographic restrictions", "Route 53 geolocation routing"],
  ["Route 53 latency routing", "S3 Transfer Acceleration", "Security groups"],
  "Filtrar por país = geo restriction de CloudFront o geolocation de Route 53.")
q(P, 2, "Which TWO actions improve read performance for a product catalog website? (Choose TWO.)",
  ["Serve images through Amazon CloudFront", "Cache frequent database queries in Amazon ElastiCache"],
  ["Enable RDS Multi-AZ", "Move images to S3 Glacier", "Add a NAT gateway"],
  "Rendimiento de lectura = CDN + caché. Multi-AZ es disponibilidad, no velocidad.")
q(P, 3, "Thousands of Lambda functions open too many connections to an RDS database and exhaust it. What should be used?",
  "Amazon RDS Proxy",
  ["A larger Lambda memory size", "RDS Multi-AZ", "Amazon SQS FIFO"],
  "Lambda + RDS + demasiadas conexiones = RDS Proxy.")
q(P, 3, "A machine-learning workload in one Availability Zone needs consistent single-digit millisecond access to S3 data with very high request rates. Which storage class fits best?",
  "S3 Express One Zone",
  ["S3 Standard-IA", "S3 Glacier Instant Retrieval", "S3 One Zone-IA"],
  "S3 con latencia de milisegundos de un dígito en UNA AZ = S3 Express One Zone.")
q(P, 2, "Write traffic to a database spikes during flash sales and some writes fail. The writes do not need to be processed immediately. What is the best solution?",
  "Put the writes into an SQS queue and process them at a steady rate",
  ["Use a larger NAT gateway", "Add read replicas", "Use CloudFront"],
  "Picos de ESCRITURA que pueden esperar = SQS como amortiguador.")

# ---------------- Optimización de costes (20 %) ----------------
C = "cost"
q(C, 1, "A company runs a steady workload on EC2 24/7 and will keep it for 3 years. Which purchasing option is the most cost-effective?",
  "A 3-year Savings Plan or Reserved Instances",
  ["On-Demand Instances", "Spot Instances", "Dedicated Hosts"],
  "Uso constante y largo = Savings Plans / Reserved (hasta ~72 % de ahorro).")
q(C, 1, "A batch job can be stopped and restarted at any time and must run at the lowest cost. Which option should be used?",
  "Spot Instances",
  ["On-Demand Instances", "Reserved Instances", "Dedicated Instances"],
  "Interrumpible + lo más barato = Spot (hasta ~90 % de ahorro).")
q(C, 1, "Data is accessed rarely but must be available in milliseconds when needed. It must survive the loss of an Availability Zone. Which S3 storage class is most cost-effective?",
  "S3 Standard-Infrequent Access (Standard-IA)",
  ["S3 One Zone-IA", "S3 Glacier Deep Archive", "S3 Standard"],
  "Acceso poco frecuente + milisegundos + varias AZ = Standard-IA.")
q(C, 1, "Access patterns for the data are unknown and change over time. The company wants S3 to optimize costs automatically. Which storage class should it use?",
  "S3 Intelligent-Tiering",
  ["S3 Standard", "S3 One Zone-IA", "S3 Glacier Flexible Retrieval"],
  "Patrón desconocido o cambiante = Intelligent-Tiering.")
q(C, 1, "Compliance archives are accessed less than once a year. Retrieval within 48 hours is acceptable. Which option is the cheapest?",
  "S3 Glacier Deep Archive",
  ["S3 Glacier Instant Retrieval", "S3 Standard-IA", "Amazon EFS"],
  "Lo más barato + recuperación en horas (hasta 12-48 h) = Deep Archive.")
q(C, 2, "Medical images are accessed about once a quarter but must be retrieved in milliseconds. Which storage class is most cost-effective?",
  "S3 Glacier Instant Retrieval",
  ["S3 Glacier Deep Archive", "S3 Glacier Flexible Retrieval", "S3 Standard"],
  "Archivo + milisegundos = Glacier INSTANT Retrieval.")
q(C, 1, "Objects should move to S3 Standard-IA after 30 days and be deleted after 365 days. What should be configured?",
  "S3 Lifecycle rules",
  ["S3 Replication", "S3 Object Lock", "AWS Backup"],
  "Mover o borrar por antigüedad = Lifecycle.")
q(C, 2, "A company pays high NAT gateway charges because EC2 instances in private subnets transfer large amounts of data to S3. How can it reduce costs?",
  "Create a gateway VPC endpoint for S3",
  ["Add more NAT gateways", "Use an internet gateway in the private subnet", "Enable S3 Transfer Acceleration"],
  "Tráfico S3 por NAT cuesta; el gateway endpoint es gratis.")
q(C, 2, "Which service analyzes utilization and recommends right-sizing EC2 instances, EBS volumes and Lambda functions?",
  "AWS Compute Optimizer",
  ["AWS Budgets", "AWS CloudTrail", "Amazon Inspector"],
  "Recomendaciones de tamaño = Compute Optimizer.")
q(C, 1, "The finance team wants an alert when monthly spending is forecast to exceed $1,000. What should be used?",
  "AWS Budgets",
  ["AWS Cost Explorer only", "Amazon CloudWatch Logs", "AWS Config"],
  "Alertas de gasto = Budgets. Cost Explorer es para analizar.")
q(C, 2, "Managers want to see costs per project and department. What should the company do?",
  "Apply cost allocation tags and analyze them in AWS Cost Explorer",
  ["Create one VPC per project", "Use AWS Shield", "Enable S3 Versioning"],
  "Costes por proyecto = etiquetas de asignación de costes + Cost Explorer.")
q(C, 1, "Development EC2 instances are used only during business hours on weekdays. How can costs be reduced?",
  "Stop the instances outside business hours automatically, for example with an EventBridge schedule",
  ["Buy 3-year Reserved Instances", "Use Dedicated Hosts", "Move them to a larger instance type"],
  "Recursos que no se usan de noche = apagarlos con un programador.")
q(C, 1, "A function runs only a few times per day for a few seconds. What is the most cost-effective compute option?",
  "AWS Lambda",
  ["An On-Demand EC2 instance running all day", "A Reserved Instance", "An EKS cluster"],
  "Uso esporádico = Lambda (pagas por ejecución).")
q(C, 2, "A company serves large files to users worldwide directly from S3 and pays high data transfer costs. What can reduce cost and improve performance?",
  "Serve the files through Amazon CloudFront",
  ["Enable S3 Versioning", "Use S3 Object Lock", "Move the files to EBS"],
  "CloudFront cachea cerca del usuario y abarata la transferencia de salida.")
q(C, 2, "A DynamoDB table has steady, predictable traffic all day. Which capacity mode is usually cheapest?",
  "Provisioned capacity with auto scaling",
  ["On-demand capacity", "DAX", "Global tables"],
  "Tráfico predecible = provisioned (más barato). Impredecible = on-demand.")
q(C, 3, "Software licensing requires the company to use its existing per-socket licenses on physical servers it can see. Which EC2 option is required?",
  "Dedicated Hosts",
  ["Spot Instances", "Dedicated Instances", "Savings Plans on shared tenancy"],
  "Licencias por socket/núcleo (BYOL) = Dedicated HOSTS. Dedicated Instances no muestran el hardware.")
q(C, 2, "Which EC2 processors usually offer the best price-performance for compatible Linux workloads?",
  "AWS Graviton (Arm-based) instances",
  ["Older generation x86 instances", "Mac instances", "Dedicated Hosts"],
  "Graviton = mejor precio-rendimiento (suele rondar un 20-40 % mejor).")
q(C, 2, "Which TWO actions reduce storage costs? (Choose TWO.)",
  ["Use S3 Lifecycle rules to move old data to S3 Glacier classes", "Delete unattached EBS volumes and old snapshots"],
  ["Convert all volumes to io2", "Enable Versioning without lifecycle rules", "Enable Multi-AZ for every database"],
  "Ahorro de almacenamiento = ciclo de vida + limpiar lo que no se usa.")
q(C, 3, "A research group shares a large dataset in S3. It wants other organizations that download the data to pay for the requests and data transfer. What should it enable?",
  "Requester Pays on the bucket",
  ["S3 Transfer Acceleration", "Cross-Region Replication", "S3 Object Lambda"],
  "Que pague quien descarga = Requester Pays.")
q(C, 2, "Files on Amazon EFS are rarely accessed after 30 days. How can storage costs be reduced automatically?",
  "Enable EFS lifecycle management to move files to EFS Infrequent Access",
  ["Move the data to EBS gp3", "Enable EFS replication", "Use EFS Max I/O mode"],
  "EFS + archivos poco usados = lifecycle a EFS-IA.")
q(C, 2, "A production RDS database will run continuously for the next year. How can the company reduce its cost?",
  "Purchase RDS Reserved Instances",
  ["Use Spot Instances for RDS", "Stop the database every night", "Enable Multi-AZ"],
  "RDS 24/7 por 1-3 años = Reserved Instances de RDS.")
q(C, 2, "Thumbnails can be regenerated from the originals if lost and are rarely accessed. Which S3 storage class is cheapest?",
  "S3 One Zone-Infrequent Access",
  ["S3 Standard", "S3 Standard-IA", "S3 Intelligent-Tiering"],
  "Datos recreables + poco acceso = One Zone-IA (más barato, una sola AZ).")
q(C, 3, "A development database is idle most of the day and receives only occasional queries. The team wants to pay as little as possible while keeping a relational database. What should it use?",
  "Amazon Aurora Serverless v2 configured with a low minimum capacity",
  ["A large provisioned RDS instance", "Amazon Redshift", "Two RDS instances in Multi-AZ"],
  "Relacional con uso esporádico = Aurora Serverless v2 (escala hacia abajo cuando está inactiva).")

# ---------------- Ampliación (temas que también caen) ----------------
q(S, 2, "Premium video files are delivered through CloudFront. Only paying users may download each file, and each link must expire. What should be used?",
  "CloudFront signed URLs", ["S3 presigned URLs without CloudFront", "A public S3 bucket", "AWS WAF rate-based rules"],
  "Contenido privado vía CloudFront = signed URLs (un archivo) o signed cookies (muchos archivos).")
q(S, 3, "A mobile app's signed-in users must upload photos directly to their own folder in S3 using temporary AWS credentials. What should be used?",
  "Amazon Cognito identity pools that exchange tokens for temporary IAM credentials", ["IAM users for each app user", "A single access key embedded in the app", "S3 Block Public Access"],
  "Usuarios de app que necesitan credenciales AWS temporales = Cognito IDENTITY pools. User pools solo autentican.")
q(S, 2, "Encrypted data must be decrypted in two Regions with the same key material. Which KMS feature helps?",
  "KMS multi-Region keys", ["SSE-S3", "CloudHSM in one Region", "Secrets Manager rotation"],
  "La misma clave en varias regiones = KMS multi-Region keys.")
q(S, 1, "A team must capture information about IP traffic going to and from network interfaces in a VPC for troubleshooting. What should be enabled?",
  "VPC Flow Logs", ["AWS CloudTrail", "AWS Config", "Amazon Macie"],
  "Tráfico IP de la VPC = Flow Logs. Llamadas a la API = CloudTrail.")
q(S, 2, "Containers in an Amazon ECS task need to read from an S3 bucket. Different tasks need different permissions. How should permissions be granted?",
  "Assign an IAM task role to each ECS task definition", ["Use the EC2 instance profile for all tasks", "Store access keys in the container image", "Make the bucket public"],
  "Permisos por contenedor en ECS = task role (no el rol de la instancia).")
q(S, 2, "Partners must upload files using SFTP. The files must land in Amazon S3 and the company does not want to manage servers. What should be used?",
  "AWS Transfer Family", ["An EC2 instance running an SFTP server", "AWS DataSync", "Amazon AppFlow"],
  "SFTP/FTPS gestionado hacia S3 o EFS = Transfer Family.")
q(S, 3, "Several AWS accounts need a single bill and shared volume discounts. What should the company use?",
  "AWS Organizations consolidated billing", ["AWS Budgets", "Cost allocation tags only", "AWS Control Tower guardrails"],
  "Una factura para muchas cuentas + descuentos por volumen = facturación consolidada de Organizations.")
q(S, 2, "A company wants to set up a secure multi-account environment quickly, with guardrails and account vending based on best practices. Which service should it use?",
  "AWS Control Tower", ["AWS Config alone", "IAM Identity Center alone", "AWS Trusted Advisor"],
  "Landing zone multicuenta con guardrails = Control Tower.")
q(S, 1, "Amazon S3 now encrypts new objects by default. Which encryption is applied if nothing else is configured?",
  "SSE-S3 (Amazon S3 managed keys)", ["SSE-KMS with a customer managed key", "SSE-C", "No encryption"],
  "Desde 2023 S3 cifra todo por defecto con SSE-S3. Si piden auditar o controlar la clave, cambia a SSE-KMS.")
q(R, 2, "VPC A is peered with VPC B, and VPC B is peered with VPC C. Instances in VPC A cannot reach VPC C. Why?",
  "VPC peering is not transitive", ["Security groups block all peering traffic", "Peering only works across Regions", "VPC C needs an internet gateway"],
  "El peering NO es transitivo: A-C necesita su propio peering o un Transit Gateway.")
q(R, 2, "A company wants to send 10% of traffic to a new version of an application and 90% to the current version. Which Route 53 routing policy should it use?",
  "Weighted routing", ["Latency routing", "Failover routing", "Geoproximity routing"],
  "Repartir por porcentajes (canary) = weighted.")
q(R, 1, "The company's root domain example.com must point to an Application Load Balancer. Which Route 53 record should be used?",
  "An alias record", ["A CNAME record at the zone apex", "An MX record", "A TXT record"],
  "Dominio raíz → recurso AWS = alias (gratis). CNAME no vale en el apex.")
q(R, 2, "Workers take messages from an SQS queue but processing sometimes takes longer than expected, so other workers process the same message again. What should be changed?",
  "Increase the queue's visibility timeout", ["Enable long polling", "Reduce the message retention period", "Switch to an SNS topic"],
  "Mensaje procesado dos veces porque tarda = subir el visibility timeout.")
q(R, 2, "Consumers of an SQS queue make many empty receive requests, which increases cost. What should be enabled?",
  "Long polling (ReceiveMessageWaitTimeSeconds > 0)", ["A FIFO queue", "A dead-letter queue", "A shorter visibility timeout"],
  "Menos respuestas vacías y menos coste = long polling.")
q(R, 2, "Before an instance is terminated by Auto Scaling, the application must upload its logs to S3. What should be used?",
  "An Auto Scaling lifecycle hook", ["A scheduled scaling action", "A larger instance", "An EBS snapshot"],
  "Hacer algo justo antes de lanzar o terminar una instancia = lifecycle hook.")
q(R, 2, "Items in a DynamoDB table must be deleted automatically 30 days after creation at no extra cost. What should be used?",
  "DynamoDB Time to Live (TTL)", ["A Lambda function scanning the table daily", "DynamoDB Streams", "AWS Backup"],
  "Borrar elementos caducados gratis = TTL.")
q(R, 3, "Every time an item changes in a DynamoDB table, a Lambda function must update a search index. What should be configured?",
  "DynamoDB Streams with a Lambda trigger", ["DynamoDB TTL", "DAX", "An SQS FIFO queue polled by EC2"],
  "Reaccionar a cambios en DynamoDB = Streams + Lambda.")
q(R, 2, "Several applications and SaaS partners need to react to events with filtering rules, without tight coupling between them. Which service fits best?",
  "Amazon EventBridge", ["Amazon SQS standard queue", "AWS Step Functions", "Amazon Kinesis Data Firehose"],
  "Bus de eventos con reglas y fuentes SaaS = EventBridge.")
q(R, 2, "A Lambda function must run every day at 2:00 a.m. What is the simplest solution?",
  "An Amazon EventBridge Scheduler schedule (or scheduled rule)", ["A cron job on an EC2 instance", "An SQS delay queue", "Step Functions running constantly"],
  "Tareas programadas sin servidores = EventBridge Scheduler.")
q(R, 1, "Developers want to deploy a web application quickly without managing infrastructure details, while AWS handles capacity, load balancing and scaling. Which service fits?",
  "AWS Elastic Beanstalk", ["Amazon EC2 with manual configuration", "AWS CloudFormation only", "Amazon Lightsail containers only"],
  "Subo el código y AWS monta lo demás = Elastic Beanstalk.")
q(R, 3, "An Aurora cluster must stay available if the writer instance fails, with failover usually completing in under a minute. What should be configured?",
  "Aurora Replicas in other Availability Zones", ["A single Aurora instance with backups", "An RDS read replica in another Region only", "DynamoDB global tables"],
  "En Aurora, las réplicas en otras AZ también son el destino del failover automático.")
q(R, 2, "A company wants its infrastructure defined as code so that identical environments can be recreated in another Region. What should it use?",
  "AWS CloudFormation", ["AWS Config", "AWS Systems Manager Session Manager", "Amazon CloudWatch"],
  "Infraestructura como código = CloudFormation (o CDK).")
q(R, 3, "On-premises offices in several countries connect to AWS through Direct Connect and must reach VPCs in multiple Regions. What should be used?",
  "A Direct Connect gateway", ["An internet gateway", "VPC peering", "A NAT gateway"],
  "Direct Connect hacia VPC de varias regiones = Direct Connect gateway.")
q(P, 2, "A company stores data in S3 and wants an ETL service that discovers schemas automatically and builds a data catalog without servers. What should it use?",
  "AWS Glue", ["Amazon EMR on EC2", "Amazon RDS", "AWS Batch"],
  "ETL sin servidores + catálogo de datos = Glue.")
q(P, 2, "Business users need interactive dashboards on data in Athena and Redshift. Which service should be used?",
  "Amazon QuickSight", ["Amazon CloudWatch dashboards", "AWS Glue", "Amazon OpenSearch Service"],
  "Paneles de negocio (BI) = QuickSight.")
q(P, 2, "An application needs full-text search and log analytics with near real-time indexing. Which service fits best?",
  "Amazon OpenSearch Service", ["Amazon Redshift", "Amazon RDS", "Amazon Neptune"],
  "Búsqueda de texto y análisis de logs = OpenSearch.")
q(P, 3, "A social network must query complex relationships such as friends of friends. Which database fits best?",
  "Amazon Neptune", ["Amazon DynamoDB", "Amazon Redshift", "Amazon Timestream"],
  "Relaciones y grafos = Neptune.")
q(P, 2, "A big data team needs to run Apache Spark and Hadoop jobs on large datasets. Which service fits best?",
  "Amazon EMR", ["AWS Glue DataBrew", "Amazon Athena", "Amazon RDS"],
  "Spark/Hadoop gestionado = EMR.")
q(P, 3, "A website must modify HTTP headers on every request at CloudFront edge locations with sub-millisecond startup at very high scale. What is the most cost-effective option?",
  "CloudFront Functions", ["Lambda@Edge", "An EC2 fleet in every Region", "API Gateway"],
  "Lógica ligera en el borde (cabeceras, redirecciones) = CloudFront Functions; algo más pesado = Lambda@Edge.")
q(P, 2, "A static website (HTML, CSS, images) must be hosted at low cost with HTTPS on a custom domain. What is the best design?",
  "Host the files in S3 and serve them through CloudFront with an ACM certificate", ["Run Apache on an EC2 instance", "Use an RDS database", "Use an EFS file system"],
  "Web estática = S3 + CloudFront (+ ACM para HTTPS).")
q(P, 2, "Repeated GET requests to a REST API in API Gateway return the same data. How can latency and backend load be reduced with minimal effort?",
  "Enable API Gateway caching", ["Increase Lambda memory", "Add a NAT gateway", "Use SQS FIFO"],
  "Respuestas repetidas en API Gateway = caché de API Gateway.")
q(P, 3, "A critical cluster application needs two EC2 instances in the same AZ to share one high-performance block volume. Which feature allows this?",
  "Amazon EBS Multi-Attach on io2 volumes", ["EBS gp3 snapshots", "Instance store", "S3 Mountpoint"],
  "Un volumen de bloque para varias instancias de la misma AZ = Multi-Attach (io1/io2).")
q(P, 2, "A company needs a managed file system that supports NFS, SMB and iSCSI with snapshots and data deduplication. Which service fits?",
  "Amazon FSx for NetApp ONTAP", ["Amazon EFS", "Amazon FSx for Lustre", "AWS Storage Gateway Volume Gateway"],
  "Multiprotocolo (NFS + SMB + iSCSI) = FSx for NetApp ONTAP.")
q(C, 2, "A company wants a free service that checks its account for cost savings, security gaps and service limits. Which service provides these recommendations?",
  "AWS Trusted Advisor", ["Amazon Inspector", "AWS Artifact", "Amazon Detective"],
  "Recomendaciones de coste, seguridad y límites = Trusted Advisor.")
q(C, 2, "EBS snapshots must be kept for years for compliance but will almost never be restored. How can storage costs be reduced?",
  "Move the snapshots to the EBS Snapshots Archive tier", ["Copy the snapshots to io2 volumes", "Keep them in the standard tier", "Convert them to AMIs"],
  "Snapshots que casi nunca se restauran = EBS Snapshots Archive (hasta un 75 % más barato).")
q(C, 2, "A Lambda function runs frequently and its cost is high. Which change can reduce cost with no code changes for most functions?",
  "Switch the function to the Arm64 (Graviton) architecture", ["Increase the timeout", "Use provisioned concurrency all day", "Add a dead-letter queue"],
  "Lambda en Arm/Graviton suele costar menos con el mismo rendimiento.")
q(C, 3, "A company needs EC2 capacity in a specific AZ for a 2-week event and must be sure it will be available. It does not want a long-term commitment. What should it use?",
  "On-Demand Capacity Reservations", ["Spot Instances", "3-year Reserved Instances", "Dedicated Hosts"],
  "Capacidad garantizada sin compromiso largo = Capacity Reservations.")
q(C, 2, "A workload runs on EC2, Fargate and Lambda and the usage mix will change over time. Which commitment gives savings across all of them?",
  "Compute Savings Plans", ["EC2 Instance Savings Plans", "Standard Reserved Instances", "Spot Instances"],
  "Ahorro flexible entre EC2, Fargate y Lambda = Compute Savings Plans.")
q(C, 1, "Which TWO options are usually the cheapest way to run a fault-tolerant, stateless batch fleet? (Choose TWO.)",
  ["Spot Instances", "Auto Scaling with mixed instance types to use spare capacity"],
  ["Dedicated Hosts", "On-Demand Instances only", "Larger instances than needed"],
  "Batch tolerante a fallos = Spot + flota diversificada para no quedarte sin capacidad.")


def main():
    rnd = random.Random(2026)
    sets = []
    for sec, lvl, text, right, wrong, e in Q:
        multi = isinstance(right, list)
        opts = (right if multi else [right]) + wrong
        order = list(range(len(opts)))
        rnd.shuffle(order)
        shuffled = [opts[i] for i in order]
        if multi:
            ans = sorted(order.index(i) for i in range(len(right)))
            qd = {"t": "multi", "q": text, "o": shuffled, "a": ans, "e": e}
        else:
            qd = {"t": "mcq", "q": text, "o": shuffled, "a": order.index(0), "e": e}
        sets.append({"sec": sec, "task": TASK[sec], "lvl": lvl, "qs": [qd]})
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "aws_a.json")
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(sets, f, ensure_ascii=False, indent=0)
    print(f"{len(sets)} preguntas AWS → {ruta}")


if __name__ == "__main__":
    main()
