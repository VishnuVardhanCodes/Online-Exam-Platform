import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store'
import { apiClient } from '../api'
import Layout from '../components/Layout'
import { Clock, BookOpen, CheckCircle, TrendingUp, Play, Eye } from 'lucide-react'

export default function StudentDashboard() {
  const navigate = useNavigate()
  const { user } = useAuthStore()
  const [quizzes, setQuizzes] = useState([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('upcoming')

  useEffect(() => {
    loadQuizzes()
  }, [activeTab])

  const loadQuizzes = async () => {
    try {
      setLoading(true)
      const response = await apiClient.getQuizzes(activeTab)
      setQuizzes(response.data.quizzes || [])
    } catch (err) {
      console.error('Failed to load quizzes:', err)
    } finally {
      setLoading(false)
    }
  }

  const getStatusBadge = (quiz: any) => {
    const now = Date.now()
    if (quiz.startTime > now) return { label: 'Upcoming', color: 'bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-200' }
    if (quiz.endTime < now) return { label: 'Ended', color: 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200' }
    return { label: 'Active', color: 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-200' }
  }

  const statCards = [
    { label: 'Available Quizzes', value: '5', icon: BookOpen, color: 'from-blue-500 to-blue-600' },
    { label: 'Completed', value: '3', icon: CheckCircle, color: 'from-green-500 to-green-600' },
    { label: 'Avg Score', value: '85%', icon: TrendingUp, color: 'from-purple-500 to-purple-600' },
    { label: 'Total Time', value: '4.5h', icon: Clock, color: 'from-orange-500 to-orange-600' },
  ]

  return (
    <Layout>
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-10">
          <h1 className="text-5xl font-bold mb-2 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Welcome back, {user?.name}! 👋
          </h1>
          <p className="text-gray-600 dark:text-gray-400 text-lg">Ready to take your next challenge? Let's get started!</p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
          {statCards.map((stat, idx) => {
            const Icon = stat.icon
            return (
              <div
                key={idx}
                className="bg-gradient-to-br dark:bg-gradient-to-br rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
              >
                <div className={`bg-gradient-to-r ${stat.color} p-1`}></div>
                <div className="bg-white dark:bg-gray-800 p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <p className="text-gray-600 dark:text-gray-400 text-sm font-medium">{stat.label}</p>
                      <p className={`text-4xl font-bold mt-2 bg-gradient-to-r ${stat.color} bg-clip-text text-transparent`}>
                        {stat.value}
                      </p>
                    </div>
                    <div className={`bg-gradient-to-r ${stat.color} p-3 rounded-lg`}>
                      <Icon className="text-white" size={24} />
                    </div>
                  </div>
                  <div className="h-1 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                    <div className={`h-full bg-gradient-to-r ${stat.color} w-3/4`}></div>
                  </div>
                </div>
              </div>
            )
          })}
        </div>

        {/* Quiz List Tabs */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden">
          {/* Tabs */}
          <div className="flex border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-700/50">
            {['upcoming', 'active', 'completed'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`flex-1 py-4 px-6 text-center font-semibold capitalize transition-all duration-300 ${
                  activeTab === tab
                    ? 'bg-white dark:bg-gray-800 text-blue-600 dark:text-blue-400 border-b-4 border-blue-600 shadow-sm'
                    : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
                }`}
              >
                {tab}
              </button>
            ))}
          </div>

          {/* Content */}
          <div className="p-6">
            {loading ? (
              <div className="flex justify-center py-12">
                <div className="w-12 h-12 border-4 border-blue-200 dark:border-blue-900 border-t-blue-600 rounded-full animate-spin"></div>
              </div>
            ) : quizzes.length === 0 ? (
              <div className="text-center py-12">
                <BookOpen className="mx-auto text-gray-400 mb-4" size={48} />
                <p className="text-gray-600 dark:text-gray-400 text-lg">No {activeTab} quizzes at the moment</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {quizzes.map((quiz: any) => {
                  const status = getStatusBadge(quiz)
                  return (
                    <div
                      key={quiz.id}
                      className="group border border-gray-200 dark:border-gray-700 rounded-xl overflow-hidden hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                    >
                      {/* Header */}
                      <div className="h-2 bg-gradient-to-r from-blue-500 to-purple-500"></div>

                      <div className="p-6">
                        {/* Title */}
                        <h3 className="text-xl font-bold mb-2 text-gray-900 dark:text-white group-hover:text-blue-600 transition-colors">
                          {quiz.title}
                        </h3>

                        {/* Description */}
                        <p className="text-gray-600 dark:text-gray-400 text-sm mb-4 line-clamp-2">
                          {quiz.description || 'No description'}
                        </p>

                        {/* Meta info */}
                        <div className="space-y-2 mb-4 text-sm text-gray-600 dark:text-gray-400">
                          <div className="flex items-center gap-2">
                            <Clock size={16} />
                            <span>{quiz.durationSeconds / 60} minutes</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <BookOpen size={16} />
                            <span>{quiz.questionIds?.length || 0} questions</span>
                          </div>
                        </div>

                        {/* Status badge */}
                        <div className="flex items-center justify-between mb-4">
                          <span className={`px-3 py-1 rounded-full text-xs font-semibold ${status.color}`}>
                            {status.label}
                          </span>
                          <span className="text-sm font-medium text-purple-600 dark:text-purple-400">
                            Attempts: {quiz.maxAttempts}
                          </span>
                        </div>

                        {/* Action buttons */}
                        <div className="flex gap-2">
                          {activeTab === 'active' ? (
                            <button 
                              onClick={() => navigate(`/quiz/${quiz.id}`)}
                              className="flex-1 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-bold py-2 px-4 rounded-lg transition-all flex items-center justify-center gap-2 transform hover:scale-105"
                            >
                              <Play size={18} />
                              Start Quiz
                            </button>
                          ) : (
                            <button className="flex-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 font-bold py-2 px-4 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-all flex items-center justify-center gap-2">
                              <Eye size={18} />
                              View Details
                            </button>
                          )}
                        </div>
                      </div>
                    </div>
                  )
                })}
              </div>
            )}
          </div>
        </div>
      </div>
    </Layout>
  )
}
