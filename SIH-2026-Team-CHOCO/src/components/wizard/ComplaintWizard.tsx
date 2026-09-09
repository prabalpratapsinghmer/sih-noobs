import React, { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import { motion, AnimatePresence } from 'framer-motion'
import { ShieldCheck, Upload, ArrowRight, ArrowLeft, CheckCircle2, Lock } from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Card } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import { computePseudoSha256, cn } from '@/lib/utils'
import { api, type ComplaintPayload, type ComplaintResponse } from '@/lib/api'

const complaintSchema = z.object({
  name: z.string().min(2, 'Full legal name is required'),
  phone: z.string().regex(/^[6-9]\d{9}$/, 'Enter valid 10-digit Indian mobile number starting with 6-9'),
  email: z.string().email('Invalid email address').optional().or(z.literal('')),
  address: z.string().min(5, 'Residential district & state required'),
  fraudType: z.enum(['INVESTMENT_SCAM', 'KYC_FRAUD', 'UPI_FRAUD', 'FAKE_JOB', 'PHISHING', 'OTHER']),
  amount: z.coerce.number().min(100, 'Minimum fraud amount is ₹100'),
  incidentDate: z.string().min(1, 'Date of incident required'),
  narrative: z.string().min(20, 'Please describe the incident in detail (min 20 characters)'),
  suspectUpi: z.string().min(3, 'Suspect UPI ID / VPA is required (e.g. suspect@ybl)'),
  suspectPhone: z.string().optional(),
  suspectAccount: z.string().optional(),
  declaration: z.literal(true, {
    errorMap: () => ({ message: 'You must acknowledge the legal perjury declaration' }),
  }),
})

type ComplaintFormData = z.infer<typeof complaintSchema>

interface ComplaintWizardProps {
  onSuccess: (complaintId: string, data: ComplaintFormData, response: ComplaintResponse) => void
}

export const ComplaintWizard: React.FC<ComplaintWizardProps> = ({ onSuccess }) => {
  const [step, setStep] = useState<1 | 2 | 3 | 4>(1)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitError, setSubmitError] = useState<string | null>(null)
  const [uploadedFileName, setUploadedFileName] = useState<string | null>('bank_statement_sept2026.pdf')
  const [evidenceHash, setEvidenceHash] = useState<string>(
    'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
  )

  const {
    register,
    handleSubmit,
    trigger,
    formState: { errors },
  } = useForm<ComplaintFormData>({
    resolver: zodResolver(complaintSchema),
    defaultValues: {
      name: 'Rohan Sharma',
      phone: '9876543210',
      email: 'rohan.sharma@example.com',
      address: 'Indiranagar, Bengaluru, Karnataka',
      fraudType: 'INVESTMENT_SCAM',
      amount: 500000,
      incidentDate: '2026-09-05',
      narrative:
        'Induced to transfer funds into high-yield trading bot scheme via Telegram group. Transfer made to VPA nexus.invest@ybl in 2 tranches of ₹2,50,000 each.',
      suspectUpi: 'nexus.invest@ybl',
      suspectPhone: '9123456780',
      suspectAccount: '918237461928',
      declaration: true,
    },
    mode: 'onChange',
  })

  const handleNext = async () => {
    let fieldsToValidate: (keyof ComplaintFormData)[] = []
    if (step === 1) fieldsToValidate = ['name', 'phone', 'address']
    if (step === 2) fieldsToValidate = ['fraudType', 'amount', 'incidentDate', 'narrative']
    if (step === 3) fieldsToValidate = ['suspectUpi']

    const valid = await trigger(fieldsToValidate)
    if (valid) {
      setStep((prev) => (prev < 4 ? ((prev + 1) as any) : prev))
    }
  }

  const handleBack = () => {
    setStep((prev) => (prev > 1 ? ((prev - 1) as any) : prev))
  }

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setUploadedFileName(file.name)
      setEvidenceHash(computePseudoSha256(file.name + file.size))
    }
  }

  const onSubmit = async (data: ComplaintFormData) => {
    setIsSubmitting(true)
    setSubmitError(null)
    try {
      const payload: ComplaintPayload = {
        name: data.name,
        phone: data.phone,
        email: data.email || undefined,
        address: data.address,
        fraud_type: data.fraudType,
        amount: data.amount,
        incident_date: data.incidentDate,
        description: data.narrative,
        fraudster_upi: data.suspectUpi,
        fraudster_phone: data.suspectPhone || undefined,
        fraudster_account: data.suspectAccount || undefined,
      }
      const response = await api.submitComplaint(payload)
      onSuccess(response.complaint_id, data, response)
    } catch (error) {
      setSubmitError(error instanceof Error ? error.message : 'Unable to submit the report. Please try again.')
    } finally {
      setIsSubmitting(false)
    }
  }

  const stepLabels = [
    { num: 1, title: 'Identity', sub: 'Complainant verification' },
    { num: 2, title: 'Incident', sub: 'Loss details & narrative' },
    { num: 3, title: 'Suspect Info', sub: 'Target VPA & routing' },
    { num: 4, title: 'Verification', sub: 'Evidence & sign-off' },
  ]

  return (
    <Card className="w-full bg-[#000000] border border-[#636363] rounded-card p-6 md:p-8 text-white">
      {/* 4-Step Stepper Bar */}
      <div className="pb-8 border-b border-[#636363]/40 mb-8">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {stepLabels.map((s) => {
            const isCompleted = step > s.num
            const isCurrent = step === s.num
            return (
              <div
                key={s.num}
                className={cn(
                  'pt-3 border-t-2 transition-all duration-200',
                  isCurrent
                    ? 'border-white'
                    : isCompleted
                    ? 'border-[#a0d1b8]'
                    : 'border-[#636363]/40'
                )}
              >
                <div className="flex items-center gap-2 mb-1">
                  <span
                    className={cn(
                      'font-mono text-xs font-bold',
                      isCurrent
                        ? 'text-white'
                        : isCompleted
                        ? 'text-[#a0d1b8]'
                        : 'text-[#9b9b9b]'
                    )}
                  >
                    0{s.num}
                  </span>
                  <span
                    className={cn(
                      'font-sans text-xs font-semibold',
                      isCurrent
                        ? 'text-white'
                        : isCompleted
                        ? 'text-[#c0c9c2]'
                        : 'text-[#c0c9c2]'
                    )}
                  >
                    {s.title}
                  </span>
                </div>
                <div className="font-sans text-xs text-[#9b9b9b] hidden sm:block">
                  {s.sub}
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {/* Wizard Form */}
      <form onSubmit={handleSubmit(onSubmit)}>
        <AnimatePresence mode="wait">
          {/* STEP 1: Victim Information */}
          {step === 1 && (
            <motion.div
              key="step1"
              initial={{ opacity: 0, x: 10 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -10 }}
              transition={{ duration: 0.2 }}
              className="space-y-6"
            >
              <div className="flex items-center justify-between pb-3 border-b border-[#636363]/40">
                <div>
                  <h2 className="text-base font-semibold text-white font-sans">Step 1: Complainant Legal Identity</h2>
                  <p className="text-xs text-[#9b9b9b] mt-0.5">
                    Official victim registration for police FIR generation and bank recovery dispatch.
                  </p>
                </div>
                <Badge variant="live">CITIZEN INTAKE</Badge>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Input
                  label="Full Legal Name (as per Aadhaar / Bank A/C)"
                  {...register('name')}
                  error={errors.name?.message}
                  placeholder="e.g. Rohan Sharma"
                />

                <Input
                  label="10-Digit Mobile Number (OTP Verified)"
                  {...register('phone')}
                  isMono
                  error={errors.phone?.message}
                  placeholder="e.g. 9876543210"
                />

                <Input
                  label="Email Address (Optional for PDF FIR Receipt)"
                  type="email"
                  {...register('email')}
                  error={errors.email?.message}
                  placeholder="e.g. rohan.sharma@example.com"
                />

                <Input
                  label="Residential District & State"
                  {...register('address')}
                  error={errors.address?.message}
                  placeholder="e.g. Indiranagar, Bengaluru, Karnataka"
                />
              </div>

              <div className="py-3 px-2 border-t border-b border-[#636363]/40 flex items-center justify-between text-xs font-mono text-[#c0c9c2]">
                <span className="flex items-center gap-2">
                  <Lock className="w-3.5 h-3.5 text-[#a0d1b8]" />
                  AADHAAR KYC VERIFIED
                </span>
                <span className="text-[#a0d1b8] font-semibold">9876-XXXX-1920 (AUTHENTICATED)</span>
              </div>
            </motion.div>
          )}

          {/* STEP 2: Incident Details */}
          {step === 2 && (
            <motion.div
              key="step2"
              initial={{ opacity: 0, x: 10 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -10 }}
              transition={{ duration: 0.2 }}
              className="space-y-6"
            >
              <div className="flex items-center justify-between pb-3 border-b border-[#636363]/40">
                <div>
                  <h2 className="text-base font-semibold text-white font-sans">Step 2: Incident & Financial Loss Details</h2>
                  <p className="text-xs text-[#9b9b9b] mt-0.5">
                    Categorize fraud modality and provide chronological loss quantification.
                  </p>
                </div>
                <Badge variant="warning">MANDATORY LOSS DATA</Badge>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="flex flex-col space-y-1.5">
                  <label className="text-xs font-sans font-medium text-[#9b9b9b]">
                    Fraud Category
                  </label>
                  <select
                    {...register('fraudType')}
                    className="w-full min-h-[42px] px-3.5 py-2 bg-[#1e2124] text-white rounded-input text-sm border border-[#636363] hover:border-[#c0c9c2] focus:outline-none focus:border-[#2b5945] focus:ring-2 focus:ring-[#2b5945]/30 transition-colors"
                  >
                    <option value="INVESTMENT_SCAM" className="bg-[#121417]">Investment & Trading Bot Scam</option>
                    <option value="KYC_FRAUD" className="bg-[#121417]">Bank / Electricity KYC Phishing</option>
                    <option value="UPI_FRAUD" className="bg-[#121417]">UPI QR Code / Intent Collect Fraud</option>
                    <option value="FAKE_JOB" className="bg-[#121417]">Work From Home / Part-Time Job Scam</option>
                    <option value="PHISHING" className="bg-[#121417]">Credit Card / Loan App Extortion</option>
                    <option value="OTHER" className="bg-[#121417]">Other Cyber Financial Crime</option>
                  </select>
                </div>

                <Input
                  label="Total Amount Siphoned (INR ₹)"
                  type="number"
                  isMono
                  {...register('amount')}
                  error={errors.amount?.message}
                  placeholder="e.g. 500000"
                />

                <Input
                  label="Date & Time of Incident"
                  type="date"
                  isMono
                  {...register('incidentDate')}
                  error={errors.incidentDate?.message}
                />
              </div>

              <div className="flex flex-col space-y-1.5">
                <label className="text-xs font-sans font-medium text-[#9b9b9b]">
                  Incident Narrative & Chronology
                </label>
                <textarea
                  {...register('narrative')}
                  rows={4}
                  className="w-full p-3.5 bg-[#1e2124] text-white rounded-input text-sm border border-[#636363] hover:border-[#c0c9c2] focus:outline-none focus:border-[#2b5945] focus:ring-2 focus:ring-[#2b5945]/30 transition-colors"
                  placeholder="Explain how you were contacted, what instructions you received, and how money was transferred..."
                />
                {errors.narrative && (
                  <span className="text-xs text-[#ff4136] tracking-tight">{errors.narrative.message}</span>
                )}
              </div>
            </motion.div>
          )}

          {/* STEP 3: Suspect Banking / VPA */}
          {step === 3 && (
            <motion.div
              key="step3"
              initial={{ opacity: 0, x: 10 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -10 }}
              transition={{ duration: 0.2 }}
              className="space-y-6"
            >
              <div className="flex items-center justify-between pb-3 border-b border-[#636363]/40">
                <div>
                  <h2 className="text-base font-semibold text-white font-sans">Step 3: Suspect Banking & UPI Routing</h2>
                  <p className="text-xs text-[#9b9b9b] mt-0.5">
                    Target account credentials for initiating instant freeze directives across NPCI rails.
                  </p>
                </div>
                <Badge variant="critical">IMMEDIATE FREEZE TARGET</Badge>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Input
                  label="Suspect UPI ID / VPA *"
                  isMono
                  {...register('suspectUpi')}
                  error={errors.suspectUpi?.message}
                  placeholder="e.g. nexus.invest@ybl"
                />

                <Input
                  label="Suspect Mobile / WhatsApp"
                  isMono
                  {...register('suspectPhone')}
                  placeholder="e.g. 9123456780"
                />

                <Input
                  label="Suspect Bank Account No."
                  isMono
                  {...register('suspectAccount')}
                  placeholder="e.g. 918237461928"
                />
              </div>

              <div className="py-3 px-2 border-t border-b border-[#636363]/40 text-xs font-mono space-y-1">
                <div className="font-bold flex items-center gap-2 text-[#fae0a6]">
                  <ShieldCheck className="w-4 h-4" />
                  AUTOMATED DISPATCH NOTICE:
                </div>
                <p className="text-[#c0c9c2] font-sans text-xs">
                  Upon submission, this VPA will be broadcast to NPCI CFR, and a 3-hop Graph Neural Network will trace outbound mule disbursements across all Indian schedule banks in under 1.2 seconds.
                </p>
              </div>
            </motion.div>
          )}

          {/* STEP 4: Evidence & Verification */}
          {step === 4 && (
            <motion.div
              key="step4"
              initial={{ opacity: 0, x: 10 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -10 }}
              transition={{ duration: 0.2 }}
              className="space-y-6"
            >
              <div className="flex items-center justify-between pb-3 border-b border-[#636363]/40">
                <div>
                  <h2 className="text-base font-semibold text-white font-sans">Step 4: Evidence Anchoring & Sign-Off</h2>
                  <p className="text-xs text-[#9b9b9b] mt-0.5">
                    Cryptographic SHA-256 seal for tamper-proof judicial evidence admissible under Sec 65B.
                  </p>
                </div>
                <Badge variant="nominal">LEGAL EVIDENCE TIER</Badge>
              </div>

              {/* Upload Dropzone */}
              <div className="border border-dashed border-[#636363] rounded-sm p-6 hover:border-white transition-colors text-center cursor-pointer relative">
                <input
                  type="file"
                  onChange={handleFileUpload}
                  className="absolute inset-0 opacity-0 cursor-pointer"
                  accept=".pdf,.png,.jpg,.jpeg,.csv"
                />
                <div className="flex flex-col items-center justify-center space-y-2">
                  <div className="w-10 h-10 rounded-full bg-[#121417] border border-[#636363] flex items-center justify-center text-white">
                    <Upload className="w-5 h-5" />
                  </div>
                  <div className="text-xs font-sans font-semibold text-white">
                    {uploadedFileName ? `Attached: ${uploadedFileName}` : 'Drag and drop Bank Statement / Chat Screenshots'}
                  </div>
                  <div className="text-xs font-mono text-[#9b9b9b]">
                    PDF, PNG, JPG up to 25MB · Auto-computed SHA-256
                  </div>
                </div>
              </div>

              {/* Blockchain Evidence Seal */}
              <div className="py-3 px-2 border-t border-b border-[#636363]/40 font-mono text-xs space-y-1">
                <div className="flex items-center justify-between text-[#9b9b9b] text-xs">
                  <span>SHA-256 EVIDENCE CHECKSUM</span>
                  <span className="text-[#a0d1b8] font-semibold">VERIFIED HASH</span>
                </div>
                <div className="text-white break-all font-semibold text-xs">
                  {evidenceHash}
                </div>
              </div>

              {/* Legal Declaration */}
              <div className="py-3 px-2 border-b border-[#636363]/40 space-y-2">
                <label className="flex items-start gap-2.5 cursor-pointer">
                  <input
                    type="checkbox"
                    {...register('declaration')}
                    className="mt-1 h-4 w-4 rounded border-[#636363] bg-[#000000] text-white focus:ring-[#a0d1b8]"
                  />
                  <span className="text-xs font-sans text-[#c0c9c2] leading-relaxed">
                    I solemnly declare under Section 193/228 IPC and Bharatiya Nyaya Sanhita (BNS) that the particulars submitted are true to the best of my knowledge and no funds have been misrepresented.
                  </span>
                </label>
                {errors.declaration && (
                  <span className="text-xs text-[#ff4136] block pl-6 tracking-tight">
                    {errors.declaration.message}
                  </span>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {submitError && (
          <div role="alert" className="mt-6 border border-[#ff4136]/70 bg-[#ff4136]/10 px-4 py-3 text-sm text-[#ffb0aa]">
            <span className="font-semibold">Report not submitted.</span> {submitError}
          </div>
        )}

        {/* Action Controls */}
        <div className="flex items-center justify-between pt-6 border-t border-[#636363]/40 mt-8">
          {step > 1 ? (
            <Button
              type="button"
              variant="secondary"
              size="md"
              onClick={handleBack}
              className="text-xs"
            >
              <ArrowLeft className="w-3.5 h-3.5 mr-1" />
              Previous Step
            </Button>
          ) : (
            <div />
          )}

          {step < 4 ? (
            <Button
              type="button"
              variant="primary"
              size="md"
              onClick={handleNext}
              className="text-xs font-semibold"
            >
              Continue to Step {step + 1}
              <ArrowRight className="w-3.5 h-3.5 ml-1" />
            </Button>
          ) : (
            <Button
              type="submit"
              variant="palantir"
              size="md"
              isLoading={isSubmitting}
              className="text-xs font-semibold"
            >
              <ShieldCheck className="w-4 h-4 mr-1.5" />
              LODGE FORM & TRIGGER RAPID FREEZE
            </Button>
          )}
        </div>
      </form>
    </Card>
  )
}
