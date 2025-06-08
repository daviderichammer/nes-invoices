import React, { useState, useEffect, useMemo } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './components/ui/card'
import { Button } from './components/ui/button'
import { Input } from './components/ui/input'
import { Badge } from './components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs'
import { 
  Search, 
  FileText, 
  DollarSign, 
  Clock, 
  TrendingUp, 
  Calendar,
  Download,
  Filter,
  BarChart3,
  PieChart
} from 'lucide-react'
import { motion } from 'framer-motion'
import './App.css'
import invoiceData from './assets/invoice_database.csv?raw'
import analyticsImage from './assets/invoice_analytics_dashboard.png'

function App() {
  const [invoices, setInvoices] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedInvoice, setSelectedInvoice] = useState(null)
  const [loading, setLoading] = useState(true)

  // Parse CSV data
  useEffect(() => {
    const parseCSV = (csvText) => {
      const lines = csvText.trim().split('\n')
      const headers = lines[0].split(',')
      
      return lines.slice(1).map(line => {
        const values = line.split(',')
        const invoice = {}
        headers.forEach((header, index) => {
          invoice[header] = values[index] || ''
        })
        return invoice
      })
    }

    try {
      const parsedData = parseCSV(invoiceData)
      setInvoices(parsedData)
      setLoading(false)
    } catch (error) {
      console.error('Error parsing CSV:', error)
      setLoading(false)
    }
  }, [])

  // Filter invoices based on search term
  const filteredInvoices = useMemo(() => {
    if (!searchTerm) return invoices
    
    return invoices.filter(invoice => 
      invoice.invoice_number?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      invoice.date?.includes(searchTerm) ||
      invoice.total_amount?.includes(searchTerm)
    )
  }, [invoices, searchTerm])

  // Calculate summary statistics
  const summaryStats = useMemo(() => {
    const totalAmount = invoices.reduce((sum, inv) => sum + parseFloat(inv.total_amount || 0), 0)
    const totalHours = invoices.reduce((sum, inv) => sum + parseInt(inv.hours || 0), 0)
    const avgRate = totalHours > 0 ? totalAmount / totalHours : 0
    
    return {
      totalInvoices: invoices.length,
      totalAmount,
      totalHours,
      avgRate
    }
  }, [invoices])

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <motion.div 
          className="text-center"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading invoice data...</p>
        </motion.div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <motion.header 
        className="bg-white shadow-lg border-b"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="bg-blue-600 p-2 rounded-lg">
                <FileText className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">NES Invoice Management</h1>
                <p className="text-gray-600">W3Evolutions Invoice Dashboard</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Badge variant="secondary" className="px-3 py-1">
                {invoices.length} Invoices
              </Badge>
              <Button variant="outline" size="sm">
                <Download className="h-4 w-4 mr-2" />
                Export
              </Button>
            </div>
          </div>
        </div>
      </motion.header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Summary Cards */}
        <motion.div 
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <Card className="bg-white shadow-lg hover:shadow-xl transition-shadow duration-300">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Total Revenue</CardTitle>
              <DollarSign className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-gray-900">
                ${summaryStats.totalAmount.toLocaleString()}
              </div>
              <p className="text-xs text-gray-500 mt-1">
                Across {summaryStats.totalInvoices} invoices
              </p>
            </CardContent>
          </Card>

          <Card className="bg-white shadow-lg hover:shadow-xl transition-shadow duration-300">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Total Hours</CardTitle>
              <Clock className="h-4 w-4 text-blue-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-gray-900">
                {summaryStats.totalHours.toLocaleString()}
              </div>
              <p className="text-xs text-gray-500 mt-1">
                Billable hours logged
              </p>
            </CardContent>
          </Card>

          <Card className="bg-white shadow-lg hover:shadow-xl transition-shadow duration-300">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Average Rate</CardTitle>
              <TrendingUp className="h-4 w-4 text-purple-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-gray-900">
                ${summaryStats.avgRate.toFixed(2)}/hr
              </div>
              <p className="text-xs text-gray-500 mt-1">
                Effective hourly rate
              </p>
            </CardContent>
          </Card>

          <Card className="bg-white shadow-lg hover:shadow-xl transition-shadow duration-300">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Date Range</CardTitle>
              <Calendar className="h-4 w-4 text-orange-600" />
            </CardHeader>
            <CardContent>
              <div className="text-lg font-bold text-gray-900">
                2023-2024
              </div>
              <p className="text-xs text-gray-500 mt-1">
                Invoice period
              </p>
            </CardContent>
          </Card>
        </motion.div>

        {/* Main Content */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <Tabs defaultValue="invoices" className="space-y-6">
            <TabsList className="grid w-full grid-cols-3 lg:w-[400px]">
              <TabsTrigger value="invoices" className="flex items-center space-x-2">
                <FileText className="h-4 w-4" />
                <span>Invoices</span>
              </TabsTrigger>
              <TabsTrigger value="analytics" className="flex items-center space-x-2">
                <BarChart3 className="h-4 w-4" />
                <span>Analytics</span>
              </TabsTrigger>
              <TabsTrigger value="reports" className="flex items-center space-x-2">
                <PieChart className="h-4 w-4" />
                <span>Reports</span>
              </TabsTrigger>
            </TabsList>

            {/* Invoices Tab */}
            <TabsContent value="invoices" className="space-y-6">
              {/* Search and Filter */}
              <Card className="bg-white shadow-lg">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Search className="h-5 w-5" />
                    <span>Search & Filter</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-col sm:flex-row gap-4">
                    <div className="flex-1">
                      <Input
                        placeholder="Search by invoice number, date, or amount..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="w-full"
                      />
                    </div>
                    <Button variant="outline" className="flex items-center space-x-2">
                      <Filter className="h-4 w-4" />
                      <span>Filters</span>
                    </Button>
                  </div>
                </CardContent>
              </Card>

              {/* Invoice List */}
              <Card className="bg-white shadow-lg">
                <CardHeader>
                  <CardTitle>Invoice List</CardTitle>
                  <CardDescription>
                    {filteredInvoices.length} of {invoices.length} invoices
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4 max-h-96 overflow-y-auto">
                    {filteredInvoices.map((invoice, index) => (
                      <motion.div
                        key={invoice.invoice_number}
                        className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 cursor-pointer transition-colors"
                        onClick={() => setSelectedInvoice(invoice)}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.3, delay: index * 0.05 }}
                        whileHover={{ scale: 1.02 }}
                      >
                        <div className="flex items-center space-x-4">
                          <div className="bg-blue-100 p-2 rounded-lg">
                            <FileText className="h-4 w-4 text-blue-600" />
                          </div>
                          <div>
                            <p className="font-semibold text-gray-900">{invoice.invoice_number}</p>
                            <p className="text-sm text-gray-500">{invoice.date}</p>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="font-semibold text-gray-900">
                            ${parseFloat(invoice.total_amount || 0).toLocaleString()}
                          </p>
                          <p className="text-sm text-gray-500">
                            {invoice.hours} hours
                          </p>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Analytics Tab */}
            <TabsContent value="analytics" className="space-y-6">
              <Card className="bg-white shadow-lg">
                <CardHeader>
                  <CardTitle>Analytics Dashboard</CardTitle>
                  <CardDescription>
                    Visual analysis of invoice data and trends
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="w-full">
                    <img 
                      src={analyticsImage} 
                      alt="Invoice Analytics Dashboard" 
                      className="w-full h-auto rounded-lg border shadow-sm"
                    />
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Reports Tab */}
            <TabsContent value="reports" className="space-y-6">
              <Card className="bg-white shadow-lg">
                <CardHeader>
                  <CardTitle>Reports & Insights</CardTitle>
                  <CardDescription>
                    Detailed analysis and business insights
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-4">
                      <h3 className="text-lg font-semibold">Key Insights</h3>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span className="text-gray-600">Highest Invoice:</span>
                          <span className="font-semibold">
                            ${Math.max(...invoices.map(inv => parseFloat(inv.total_amount || 0))).toLocaleString()}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Average Invoice:</span>
                          <span className="font-semibold">
                            ${(summaryStats.totalAmount / summaryStats.totalInvoices).toLocaleString()}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Most Hours (Single Invoice):</span>
                          <span className="font-semibold">
                            {Math.max(...invoices.map(inv => parseInt(inv.hours || 0)))} hours
                          </span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="space-y-4">
                      <h3 className="text-lg font-semibold">Performance Metrics</h3>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span className="text-gray-600">Revenue Growth:</span>
                          <Badge variant="secondary" className="bg-green-100 text-green-800">
                            Positive Trend
                          </Badge>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Billing Efficiency:</span>
                          <Badge variant="secondary" className="bg-blue-100 text-blue-800">
                            High
                          </Badge>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Client Relationship:</span>
                          <Badge variant="secondary" className="bg-purple-100 text-purple-800">
                            Long-term
                          </Badge>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </motion.div>
      </div>

      {/* Invoice Detail Modal */}
      {selectedInvoice && (
        <motion.div 
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          onClick={() => setSelectedInvoice(null)}
        >
          <motion.div 
            className="bg-white rounded-lg p-6 max-w-md w-full"
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold">Invoice Details</h3>
              <Button 
                variant="ghost" 
                size="sm"
                onClick={() => setSelectedInvoice(null)}
              >
                ×
              </Button>
            </div>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-600">Invoice Number:</span>
                <span className="font-semibold">{selectedInvoice.invoice_number}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Date:</span>
                <span className="font-semibold">{selectedInvoice.date}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Hours:</span>
                <span className="font-semibold">{selectedInvoice.hours}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Rate:</span>
                <span className="font-semibold">${selectedInvoice.unit_price}/hr</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Total Amount:</span>
                <span className="font-semibold text-lg">
                  ${parseFloat(selectedInvoice.total_amount || 0).toLocaleString()}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Terms:</span>
                <span className="font-semibold">{selectedInvoice.terms}</span>
              </div>
            </div>
          </motion.div>
        </motion.div>
      )}
    </div>
  )
}

export default App

